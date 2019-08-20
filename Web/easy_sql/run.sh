#!/bin/bash
chown www-data:www-data /app -R

if [ "$ALLOW_OVERRIDE" = "**False**" ]; then
    unset ALLOW_OVERRIDE
else
    sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf
    a2enmod rewrite
fi

# initialize database
mysqld_safe --skip-grant-tables&
sleep 5
## change root password
mysql -uroot -e "use mysql;UPDATE user SET password=PASSWORD('gaycnebkak459v') WHERE user='root';FLUSH PRIVILEGES;"
## restart mysql
service mysql restart
## execute sql file


mysql -uroot -pgaycnebkak459v < /tmp/sql.sql

rm -rf /tmp/*

sed -i "s/;session.upload_progress.enabled = On/session.upload_progress.enabled = Off/g" /etc/php5/cli/php.ini
sed -i "s/;session.upload_progress.enabled = On/session.upload_progress.enabled = Off/g" /etc/php5/apache2/php.ini

cd /etc/php5/apache2/conf.d/
rm 20-xdebug.ini
rm 20-memcached.ini
rm 20-memcache.ini

rm -r /var/www/phpinfo

source /etc/apache2/envvars
tail -F /var/log/apache2/* &
exec apache2 -D FOREGROUND
service apache2 start

chmod -R 755 /app
rm /app/logo.png
apt-get install -y vim

