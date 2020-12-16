# bunkerized-mariadb

<img src="https://github.com/bunkerity/bunkerized-mariadb/blob/master/logo.png?raw=true" width="425" />

mariadb based Docker image secure by default.

Non-exaustive list of features :
- Configure strong password policy
- Set privileges for regular user
- TLS support with automatic Let's Encrypt automation or custom certificate
- Remove default data and user
- State of the art configuration best practises
- Support of ed25519 for authentication
- Based on alpine
- Easy to configure with environment variables

# Table of contents
- [bunkerized-mariadb](#bunkerized-mariadb)
- [Table of contents](#table-of-contents)
- [Quickstart guide](#quickstart-guide)
  * [Default settings with random passwords](#default-settings-with-random-passwords)
  * [Default settings with choosen passwords](#default-settings-with-choosen-passwords)
  * [TLS support with automatic Let's Encrypt](#tls-support-with-automatic-let-s-encrypt)
- [List of environment variables](#list-of-environment-variables)
  * [Admin account](#admin-account)
  * [User account](#user-account)
  * [Passwords](#passwords)
  * [TLS](#tls)
  * [Misc](#misc)
- [Execute custom SQL files](#execute-custom-sql-files)
- [Include custom MariaDB configurations](#include-custom-mariadb-configurations)
- [TODO](#todo)

# Quickstart guide

## Default settings with random passwords

```shell
docker run -v /where/to/save/databases:/var/lib/mysql -e USER_NAME=myuser bunkerity/bunkerized-mariadb
```
- Passwords of root and myuser will be displayed on the standard output.  
- A database named myuser_db will be created with minimal privileges given to myuser.

## Default settings with choosen passwords
```shell
docker run -v /where/to/save/databases:/var/lib/mysql -e USER_NAME=myuser -e USER_PASSWORD=userpass -e ROOT_PASSWORD=rootpass bunkerity/bunkerized-mariadb
```
- The passwords must follow the password policy (default : 12 chars long, at least 1 letter, 1 digit and 1 special char)
- See the passwords environment variables to adjust the policy to your needs

## TLS support with automatic Let's Encrypt

```shell
docker run -p 3306:3306 -p 80:80 -v /where/to/save/databases:/var/lib/mysql -v /where/to/save/certificate:/etc/letsencrypt -e USER_NAME=myuser -e SERVER_NAME=my.domain.net -e AUTO_LETS_ENCRYPT=yes bunkerity
```
- my.domain.net must resolve to your server address
- port 80 needs to be opened because Let's Encrypt use it to check that you own my.domain.net

# List of environment variables

## Admin account
`ROOT_NAME`  
Values : *\<any valid username\>*  
Default value : *root*  
This is the username for the admin account. Can be interesting to set it to something different than root to counter bruteforcing if you database is available online.

`ROOT_HOST`  
Values : *%* | *\<ip address\>* | *\<domain name\>*  
Default value : *localhost*  
IP address or domain name from where the admin account can connect (% means anywhere). Only valid if `ROOT_METHOD` is set to *password* or *both*.  

`ROOT_PASSWORD`  
Values : *\<any valid password\>*
Default value : *random password*  
This is the password for the admin account. Only valid if `ROOT_METHOD` is set to *password* and it meets the password policy constraints.

`ROOT_METHOD`  
Values : *password* | *shell* | *both*  
Default value : *both*  
How the admin account can connect. If *password* is used, `ROOT_PASSWORD` must be provided. If it's *shell*, root can login directly within a shell (via unix_socket). To allow both password and shell access use *both* (the default).

## User account
`USER_NAME`  
Values : *\<any valid username\>*  
Default value :  
This is the username of the regular account to be created. By default, `USER_NAME` is blank so no regular account is created.

`USER_PASSWORD`  
Values : *\<any valid password\>*  
Default value : *random password*  
This is the password for the regular account. Only valid if `USER_NAME` is not empty and it meets the password policy constraints.

`USER_DATABASE`  
Values : *\<any valid database name\>*  
Default value : *[USER_NAME]_db*  
Name of the database to be created for the user specified in `USER_NAME`.

`USER_PRIVILEGES`  
Values : *\<list of privileges separated by comma\>*  
Default value : *ALTER, CREATE, DELETE, DROP, INDEX, INSERT, REFERENCES, SELECT, UPDATE*  
List of privileges granted to the user `USER_NAME` on the database `USER_DATABASE`.

## Passwords
`USE_AUTH_ED25519`  
Values : *yes* | *no*  
Default value : *no*  
If set to yes, will use ed25519 to store passwords and authenticate users. It's better than traditional mysql_native_password (which is based on SHA1). But not all clients support it.

`USE_SIMPLE_PASSWORD_CHECK`  
Values : *yes* | *no*  
Default value : *yes*  
If set to yes, will use the simple password plugin to define and check password constraints.

`PASSWORD_LENGTH`  
Values : *\<any positive numeric value\>*  
Default value : *12*  
Defines the minimum length of passwords. Only valid if `USE_SIMPLE_PASSWORD_CHECK` is set to yes.

`PASSWORD_DIGITS`  
Values : *\<any positive numeric value\>* | *0*  
Default value : *1*  
Defines the minimum number of digits in passwords. Only valid if `USE_SIMPLE_PASSWORD_CHECK` is set to yes.

`PASSWORD_LETTERS`  
Values : *\<any positive numeric value\>* | *0*  
Default value : *1*  
Defines the minimum number of letters in passwords. Only valid if `USE_SIMPLE_PASSWORD_CHECK` is set to yes.

`PASSWORD_SPECIALS`  
Values : *\<any positive numeric value\>* | *0*  
Default value : *1*  
Defines the minimum number of special characters in passwords. Only valid if `USE_SIMPLE_PASSWORD_CHECK` is set to yes.

## TLS
`AUTO_LETS_ENCRYPT`  
Values : *yes* | *no*  
Default value : *no*  
If set to yes, TLS will be enabled with automatic certificate generation and renewal through Let's Encrypt. Note that `ROOT_METHOD` must be set to *shell* or *both* to allow automatic renewal and reloading MariaDB SSL configuration.

`SERVER_NAME`  
Values : *\<your domain name\>*  
Default value : *your.domain.net*  
If `AUTO_LETS_ENCRYPT` is set to yes, you must set this to your domain name.

`SSL_CERT`  
Values : *\<any valid path to TLS server certificate file\>*  
Default value :  
If `SSL_CERT`, `SSL_KEY` and `SSL_CA` are set to valid paths, MariaDB will enable TLS with the certificate, key and CA provided in those files.

`SSL_KEY`  
Values : *\<any valid path to TLS key file\>*  
Default value :  
If `SSL_CERT`, `SSL_KEY` and `SSL_CA` are set to valid paths, MariaDB will enable TLS with the certificate, key and CA provided in those files.

`SSL_CA`  
Values : *\<any valid path to TLS CA certificate file\>*  
Default value :  
If `SSL_CERT`, `SSL_KEY` and `SSL_CA` are set to valid paths, MariaDB will enable TLS with the certificate, key and CA provided in those files.

`REQUIRE_SSL`  
Values : *yes* | *no*  
Default value : *yes*  
If set to *yes* and TLS is enabled then the regular user (if specified with `USER_NAME`) and the root account are forced to use TLS.

## Misc
`LOCAL_INFILE`  
Values : *OFF* | *ON*  
Default value : *OFF*  
If set to *OFF*, the LOAD DATA INFILE statements are disabled.

`SKIP_NAME_RESOLVE`  
Values : *OFF* | *ON*  
Default value : *ON*  
If set to *ON*, only IP addresses are used when checking the connecting client (no hostname resolved).

`SKIP_SHOW_DATABASE`  
Values : *OFF* | *ON*  
Default value : *ON*  
If set to *ON*, will deny the SHOW DATABASES statement to regular users.

`SECURE_FILE_PRIV`  
Values : *\<any path\>*  
Default value : */nowhere*  
If set to something (not blank), all LOAD DATA, SELECT ... INTO and LOAD FILE() statements will only work if the files are in this path.

`LOGROTATE_MINSIZE`  
Values : *x* | *xk* | *xM* | *xG*  
Default value : 10M  
The minimum size of a log file before being rotated (no letter = bytes, k = kilobytes, M = megabytes, G = gigabytes).

`LOGROTATE_MAXAGE`  
Values : *\<any integer\>*  
Default value : 7  
The number of days before rotated files are deleted.

# Execute custom SQL files

You can execute custom .sql files by mouting them inside the /custom.sql.d directory :

```shell
docker run ... -v /path/to/custom/sql/files:/custom.sql.d ... bunkerity/bunkerized-mariadb
```

Please note that the files will only be executed once after MariaDB has been setup. They won't be executed if a database already exists in the /var/lib/mysql directory.

# Include custom MariaDB configurations

You can add custom .cnf files by mounting them inside the /custom.cnf.d directory :

```shell
docker run ... -v /path/to/custom/cnf/files:/custom.cnf.d ... bunkerity/bunkerized-mariadb
```

# TODO
- data at rest encryption
- fail2ban ?
- libinjection ?
- compile mariadb from sources with security flags
- custom image
