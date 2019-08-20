FROM webdevops/php-nginx:5.6

RUN chown www-data:www-data /app/* -R

COPY src/html /app

COPY src/flag /flag
COPY src/clean.sh /clean.sh

RUN chmod 0700 /clean.sh

RUN echo "*/10 * * * * root bash /clean.sh">>/etc/cron.d/php && \
    chmod 0644 /etc/cron.d/php

EXPOSE 80