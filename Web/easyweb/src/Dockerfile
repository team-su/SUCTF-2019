FROM phusion/baseimage:0.11
MAINTAINER Zenis <sy5323@126.com>

RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y apache2 libapache2-mod-php7.2 php7.2-fpm php7.2-mbstring&& \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/www/html/*

RUN mkdir -p /etc/service/apache2/ && \
    printf "#!/bin/sh\n\nexec /usr/sbin/apachectl -D FOREGROUND\n" > /etc/service/apache2/run && \
    chmod 700 /etc/service/apache2/run


ADD ./www /var/www/html
ADD ./THis_Is_tHe_F14g /THis_Is_tHe_F14g
ADD ./php.ini /etc/php/7.2/apache2/php.ini
ADD ./php.ini /etc/php/7.2/fpm/php.ini
ADD ./000-default.conf /etc/apache2/sites-available/000-default.conf
ADD ./clean.sh /clean.sh

RUN chown www-data:www-data -R /var/www/html && \
    chmod 777 /var/www/html/upload


RUN chmod 444 /THis_Is_tHe_F14g && \
    echo "*/20 * * * * root bash /clean.sh">>/etc/cron.d/php && \
    chmod 0644 /etc/cron.d/php

EXPOSE 80
