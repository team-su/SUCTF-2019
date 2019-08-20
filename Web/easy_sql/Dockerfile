FROM andreisamuilik/php5.5.9-apache2.4-mysql5.5

ADD file /app/
RUN apt-get update
RUN a2enmod rewrite
COPY run.sh /run.sh
COPY sql.sql /tmp/sql.sql
RUN chmod +x /run.sh

CMD ["/run.sh"]

