FROM phusion/baseimage:latest

RUN apt-get update && apt-get install -y python-software-properties && add-apt-repository ppa:ondrej/php && apt-get update

RUN apt-get install -y php5.6 php5.6-mbstring php5.6-curl php5.6-cli php5.6-mysql php5.6-soap libapache2-mod-php5.6 mariadb-server apache2 gcc netcat-traditional && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/www/html/*

COPY src/php.ini /etc/php/5.6/cli/php.ini
RUN mkdir -p /etc/service/apache2/ && \
    printf "#!/bin/sh\n\nexec /usr/sbin/apachectl -D FOREGROUND\n" > /etc/service/apache2/run && \
    mkdir -p /etc/service/mysql/ && \
    printf "#!/bin/sh\n\nexec /usr/bin/mysqld_safe\n" > /etc/service/mysql/run && \
    mkdir -p /var/run/mysqld/ && chown mysql:mysql /var/run/mysqld && \
    chmod 700 /etc/service/mysql/run /etc/service/apache2/run

COPY src/html /var/www/html
COPY src/flag /flag
COPY src/readflag.c /readflag.c
RUN chmod 600 /flag && chmod 777 /var/www/html/upload

RUN gcc /readflag.c -o /readflag && \
    chmod +s /readflag

EXPOSE 80