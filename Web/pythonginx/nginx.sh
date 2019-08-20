#! /usr/bin/env bash

# Max File Uplaod
set -e
echo "client_max_body_size 0;" > /etc/nginx/conf.d/upload.conf
echo "127.0.0.1     suctf.cc" >> /etc/hosts

# Static Files Setup
USE_STATIC_URL=${STATIC_URL:-'/static'}
USE_STATIC_PATH=${STATIC_PATH:-'/app/static'}

# Generate Nginx config
echo "server {
    listen 80;
    location / {
        try_files \$uri @app;
    }
    location @app {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/uwsgi.sock;
    }
    location $USE_STATIC_URL {
        alias $USE_STATIC_PATH;
    }" > /etc/nginx/conf.d/nginx.conf

if [[ $STATIC_INDEX == 1 ]] ; then
echo "    location = / {
        index $USE_STATIC_URL/index.html;
    }" >> /etc/nginx/conf.d/nginx.conf
fi

# Finish the Nginx config file
echo "}" >> /etc/nginx/conf.d/nginx.conf

exec "$@"
