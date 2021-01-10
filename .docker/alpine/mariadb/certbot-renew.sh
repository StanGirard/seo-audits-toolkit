#!/bin/sh

certbot renew

cp /etc/letsencrypt/live/*/fullchain.pem /opt/letsencrypt/ca.pem
cp /etc/letsencrypt/live/*/cert.pem /opt/letsencrypt/cert.pem
openssl rsa -in /etc/letsencrypt/live/*/privkey.pem -out /opt/letsencrypt/key.pem
chown root:mysql /opt/letsencrypt/*.pem
chmod 640 /opt/letsencrypt/*.pem

if [ -f /var/lib/mysql/$(hostname).pid ] ; then
	mysql -e "FLUSH SSL;"
fi
