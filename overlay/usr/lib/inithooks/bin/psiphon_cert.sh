#!/bin/sh

echo "####################################################"
echo "### Creating SSL certificate and key for Psiphon ###"
echo "####################################################"

#This prompts for domain name or IP address

openssl req -nodes -x509 -new -out /opt/psiphon/apache2/ssl/psiphon2.crt -keyout /opt/psiphon/apache2/ssl/psiphon2.key -days 365 -config /etc/psiphon/openssl.cnf -newkey rsa:2048
