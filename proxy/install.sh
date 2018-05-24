#!/bin/bash

# install apache with https redirection and self signed cert
apt install apache2
/etc/init.d/apache2 restart
a2enmod rewrite proxy proxy_http ssl
mkdir /etc/apache2/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj '/CN=local/O=local/C=US' -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt
cat > /etc/apache2/sites-available/default-ssl.conf <<EOL
<IfModule mod_ssl.c>
    <VirtualHost *:443>
        ServerName www.domain.com
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
        SSLEngine on
        SSLCertificateFile /etc/apache2/ssl/apache.crt
        SSLCertificateKeyFile /etc/apache2/ssl/apache.key
        <FilesMatch "\.(cgi|shtml|phtml|php)$">
                        SSLOptions +StdEnvVars
        </FilesMatch>
        <Directory /usr/lib/cgi-bin>
                        SSLOptions +StdEnvVars
        </Directory>
        BrowserMatch "MSIE [2-6]" \
                        nokeepalive ssl-unclean-shutdown \
                        downgrade-1.0 force-response-1.0
        BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown
        SSLProxyEngine On
        ProxyPass / https://c2.com/
        ProxyPassReverse / https://c2.com/
        SSLProxyCheckPeerCN off
        SSLProxyCheckPeerName off
        SSLProxyCheckPeerExpire off
    </VirtualHost>
</IfModule>
EOL
a2ensite default-ssl.conf
/etc/init.d/apache2 restart

# (OPTIONAL) create certificate for apache using let's encrypt
apt install software-properties-common
add-apt-repository ppa:certbot/certbot
apt update
apt install python-certbot-apache 
certbot --apache
#certbot --apache certonly
#certbot renew --dry-run
/etc/init.d/apache2 restart
