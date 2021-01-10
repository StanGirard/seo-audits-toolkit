#!/bin/sh

# replace pattern in file
function replace_in_file() {
	# escape slashes
	pattern=$(echo "$2" | sed "s/\//\\\\\//g")
	replace=$(echo "$3" | sed "s/\//\\\\\//g")
	sed -i "s/$pattern/$replace/g" "$1"
}

# check if a pass meets the constraints
function check_pass() {
	if [ ${#1} -lt $PASSWORD_LENGTH ] ; then
		return 1
	fi
	check=$(echo "$1" | tr -dc '0-9')
	if [ ${#check} -lt $PASSWORD_DIGITS ] ; then
		return 1
	fi
	check=$(echo "$1" | tr -dc 'a-z')
	if [ ${#check} -lt $PASSWORD_LETTERS ] ; then
		return 1
	fi
	check=$(echo "$1" | tr -dc 'A-Z')
	if [ ${#check} -lt $PASSWORD_LETTERS ] ; then
		return 1
	fi
	check=$(echo "$1" | tr -dc '!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~')
	if [ ${#check} -lt $PASSWORD_SPECIALS ] ; then
		return 1
	fi
	return 0
}

# generate a random pass and check constraints
function random_pass() {
	while [ 1 ] ; do
		pass=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9!#$&()*+,-./:;<=>?@[]^`{|}~' | fold -w $PASSWORD_LENGTH | head -n 1)
		check_pass "$pass"
		if [ $? -eq 0 ] ; then
			break
		fi
	done
	echo "$pass"
}

# trap SIGTERM and SIGINT
function trap_exit() {
        echo "[*] Catched stop operation"
        echo "[*] Stopping crond ..."
        pkill -TERM crond
        echo "[*] Stopping mariadb ..."
        mysqladmin shutdown
        pkill -TERM tail
}
trap "trap_exit" TERM INT

# default values
ROOT_NAME="${ROOT_NAME-root}"
ROOT_HOST="${ROOT_HOST-localhost}"
ROOT_METHOD="${ROOT_METHOD-both}"
USER_DATABASE="${USER_DATABASE-${USER_NAME}_db}"
USER_PRIVILEGES="${USER_PRIVILEGES-ALTER, CREATE, DELETE, DROP, INDEX, INSERT, REFERENCES, SELECT, UPDATE}"
USE_AUTH_ED25519="${USE_AUTH_ED25519-no}"
USE_SIMPLE_PASSWORD_CHECK="${USE_SIMPLE_PASSWORD_CHECK-yes}"
PASSWORD_LENGTH="${PASSWORD_LENGTH-12}"
PASSWORD_DIGITS="${PASSWORD_DIGITS-1}"
PASSWORD_LETTERS="${PASSWORD_LETTERS-1}"
PASSWORD_SPECIALS="${PASSWORD_SPECIALS-1}"
AUTO_LETS_ENCRYPT="${AUTO_LETS_ENCRYPT-no}"
SERVER_NAME="${SERVER_NAME-your.domain.net}"
REQUIRE_SECURE_TRANSPORT="${REQUIRE_SECURE_TRANSPORT-ON}"
LOCAL_INFILE="${LOCAL_INFILE-OFF}"
SKIP_NAME_RESOLVE="${SKIP_NAME_RESOLVE-ON}"
SKIP_SHOW_DATABASE="${SKIP_SHOW_DATABASE-ON}"
SECURE_FILE_PRIV="${SECURE_FILE_PRIV-/nowhere}"
REQUIRE_SSL="${REQUIRE_SSL-yes}"

# remove cron jobs
echo "" > /etc/crontabs/root

# copy stub confs
cp /opt/logrotate.conf /etc/logrotate.conf
LOGROTATE_MINSIZE="${LOGROTATE_MINSIZE-10M}"
LOGROTATE_MAXAGE="${LOGROTATE_MAXAGE-7}"

# setup log file
if [ ! -f "/var/log/mariadb.log" ] ; then
	touch /var/log/mariadb.log
	chmod 760 /var/log/mariadb.log
	chown root:mysql /var/log/mariadb.log
fi


# check if there is already some data or no
FIRST_INSTALL="yes"
if [ "$(ls /var/lib/mysql)" ] ; then
	FIRST_INSTALL="no"
fi

# stuff to do only on first install
if [ "$FIRST_INSTALL" = "yes" ] ; then
	# random ROOT_PASSWORD if not set
	if [ -z "$ROOT_PASSWORD" ] && { [ "$ROOT_METHOD" = "password" ] || [ "$ROOT_METHOD" = "both" ]; } ; then
		echo "[*] ROOT_PASSWORD is not set, random one will be generated."
		ROOT_PASSWORD=$(random_pass)
		echo "[*] generated $ROOT_NAME password : $ROOT_PASSWORD"
	# check policy otherwise
	elif [ "$USE_SIMPLE_PASSWORD_CHECK" = "yes" ] && { [ "$ROOT_METHOD" = "password" ] || [ "$ROOT_METHOD" = "both" ]; } ; then
		check_pass "$ROOT_PASSWORD"
		if [ $? -ne 0 ] ; then
			echo "ROOT_PASSWORD does not meet the policy requirements."
			exit 1
		fi
	fi

	# random user password if needed
	if [ ! -z "$USER_NAME" ] && [ -z "$USER_PASSWORD" ] ; then
		echo "[*] USER_NAME is set but USER_PASSWORD isn't, random one will be generated."
		USER_PASSWORD=$(random_pass)
		echo "[*] generated $USER_NAME password : $USER_PASSWORD"
		#USER_PASSWORD=$(echo $USER_PASSWORD | sed s/'\\'/'\\\\'/g | sed s/"'"/"\\\'"/g)
	# check policy otherwise
	elif [ ! -z "$USER_NAME" ] && [ "$USE_SIMPLE_PASSWORD_CHECK" = "yes" ] ; then
		check_pass "$USER_PASSWORD"
		if [ $? -ne 0 ] ; then
			echo "USER_PASSWORD does not meet the policy requirements."
			exit 1
		fi
	fi

	# initialize database
	echo "[*] initializing system databases ..."
	mysql_install_db --skip-test-db --user=mysql --datadir=/var/lib/mysql > /dev/null

fi

# edit config depending on variables and setup TLS
cp /opt/mariadb-server.cnf /etc/my.cnf.d/mariadb-server.cnf
if [ "$USE_AUTH_ED25519" = "yes" ] ; then
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#plugin_load_add = auth" "plugin_load_add = auth"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#ed25519=" "ed25519="
fi
if [ "$USE_SIMPLE_PASSWORD_CHECK" = "yes" ] ; then
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#plugin_load_add = simple" "plugin_load_add = simple"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#simple_password" "simple_password"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%PASSWORD_DIGITS%" "$PASSWORD_DIGITS"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%PASSWORD_LETTERS%" "$PASSWORD_LETTERS"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%PASSWORD_LENGTH%" "$PASSWORD_LENGTH"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%PASSWORD_SPECIALS%" "$PASSWORD_SPECIALS"
fi
if [ "$AUTO_LETS_ENCRYPT" = "yes" ] ; then
	SSL="yes"
	if [ "$ROOT_METHOD" = "password" ] ; then
		echo "[!] You need to set ROOT_METHOD to shell or both when using auto Let's Encrypt"
	exit 1
	fi
	if [ ! -d /opt/letsencrypt ] ; then
		mkdir /opt/letsencrypt
		chown root:mysql /opt/letsencrypt
	fi
	if [ -f /etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem ] ; then
		/opt/certbot-renew.sh
	else
		certbot certonly --standalone -n --preferred-challenges http -d $SERVER_NAME --email contact@$SERVER_NAME --agree-tos
		cp /etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem /opt/letsencrypt/ca.pem
		cp /etc/letsencrypt/live/${SERVER_NAME}/cert.pem /opt/letsencrypt/cert.pem
		openssl rsa -in /etc/letsencrypt/live/${SERVER_NAME}/privkey.pem -out /opt/letsencrypt/key.pem
		chown root:mysql /opt/letsencrypt/*.pem
		chmod 640 /opt/letsencrypt/*.pem
	fi
	echo "0 0 * * * /opt/certbot-renew.sh" >> /etc/crontabs/root
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SSL_CERT%" "/opt/letsencrypt/cert.pem"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SSL_KEY%" "/opt/letsencrypt/key.pem"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SSL_CA%" "/opt/letsencrypt/ca.pem"
elif [ -n "$SSL_CERT" ] && [ -n "$SSL_KEY" ] && [ -n "$SSL_CA" ] ; then
	SSL="yes"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SSL_CERT%" "$SSL_CERT"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SSL_KEY%" "$SSL_KEY"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SSL_CA%" "$SSL_CA"
fi
if [ -n "$SSL" ] ; then
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#ssl_" "ssl_"
	replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#tls_" "tls_"
	#replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#require_secure_transport" "require_secure_transport"
fi
if [ ! -d "$SECURE_FILE_PRIV" ] ; then
	mkdir "$SECURE_FILE_PRIV"
fi
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%REQUIRE_SECURE_TRANSPORT%" "$REQUIRE_SECURE_TRANSPORT"
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#local_infile" "local_infile"
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#skip_name_resolve" "skip_name_resolve"
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#skip_show_database" "skip_show_database"
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "#secure_file_priv" "secure_file_priv"
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%LOCAL_INFILE%" "$LOCAL_INFILE"
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SKIP_NAME_RESOLVE%" "$SKIP_NAME_RESOLVE"
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SKIP_SHOW_DATABASE%" "$SKIP_SHOW_DATABASE"
replace_in_file "/etc/my.cnf.d/mariadb-server.cnf" "%SECURE_FILE_PRIV%" "$SECURE_FILE_PRIV"

# run mysqld_safe
echo "[*] starting mysqld_safe ..."
mysqld_safe &

if [ "$FIRST_INSTALL" = "yes" ] ; then
	# wait before mysqld initialize
	sleep 3

	# run mysql_secure_installation
	echo "[*] executing mysql_secure_installation ..."
	echo -e "\nY\nn\nY\nY\nY\nY\n" | mysql_secure_installation

	# remove default mysql user
	mysql -e "DROP USER 'mysql'@'localhost';"

	# setup normal user
	if [ ! -z "$USER_NAME" ] ; then
		mysql -e "CREATE DATABASE $USER_DATABASE;"
		if [ "$USE_AUTH_ED25519" = "yes" ] ; then
			mysql -e "GRANT $USER_PRIVILEGES ON $USER_DATABASE.* TO '$USER_NAME'@'%' IDENTIFIED VIA ed25519 USING PASSWORD('$USER_PASSWORD');"
		else
			mysql -e "GRANT $USER_PRIVILEGES ON $USER_DATABASE.* TO '$USER_NAME'@'%' IDENTIFIED BY '$USER_PASSWORD';"
		fi
		if [ -n "$SSL" ] && [ "$REQUIRE_SSL" = "yes" ] ; then
			mysql -e "ALTER USER '$USER_NAME'@'%' REQUIRE SSL;";
		fi
	fi

	# run custom sql files
	for file in $(ls /custom.sql.d/*.sql) ; do
		mysql < "$file"
	done

	# setup root user
	if [ "$USE_AUTH_ED25519" = "yes" ] && { [ "$ROOT_METHOD" = "password" ] || [ "$ROOT_METHOD" = "both" ]; } ; then
		mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$ROOT_NAME'@'$ROOT_HOST' IDENTIFIED VIA ed25519 USING PASSWORD('$ROOT_PASSWORD') WITH GRANT OPTION;"
	elif [ "$ROOT_METHOD" = "password" ] || [ "$ROOT_METHOD" = "both" ] ; then
		mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$ROOT_NAME'@'$ROOT_HOST' IDENTIFIED BY '$ROOT_PASSWORD' WITH GRANT OPTION;"
	fi
	if [ -n "$SSL" ] && [ "$REQUIRE_SSL" = "yes" ] && { [ "$ROOT_METHOD" = "password" ] || [ "$ROOT_METHOD" = "both" ]; } ; then
		mysql -e "ALTER USER '$ROOT_NAME'@'$ROOT_HOST' REQUIRE SSL;";
	fi
	if [ "$ROOT_METHOD" = "password" ] ; then
		mysql -e "DELETE FROM mysql.user WHERE plugin = 'unix_socket';"
	fi

	# reload privileges
	mysql -e "FLUSH PRIVILEGES;" 2> /dev/null
fi

# start crond
crond

# setup logrotate
replace_in_file "/etc/logrotate.conf" "%LOGROTATE_MAXAGE%" "$LOGROTATE_MAXAGE"
replace_in_file "/etc/logrotate.conf" "%LOGROTATE_MINSIZE%" "$LOGROTATE_MINSIZE"
echo "0 0 * * * logrotate -f /etc/logrotate.conf > /dev/null 2>&1" >> /etc/crontabs/root

# print logs until container stop
tail -f /var/log/mariadb.log &
wait $!

# we're done
echo "[*] bunkerized-mariadb stopped"
exit 0
