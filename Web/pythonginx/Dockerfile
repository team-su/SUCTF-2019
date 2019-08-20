FROM terrillo/python3flask:latest

# STATIC paths for file.
# Don't use flask static. Nginx is your friend
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

# Place your flask application on the server
COPY ./flag /usr/fffffflag
COPY ./nginx.conf /usr/local/nginx/conf/nginx.conf
COPY ./app /app
WORKDIR /app

# Install requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# NGINX setup
COPY ./nginx.sh /nginx.sh
RUN chmod +x /nginx.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["/nginx.sh"]

# Start Server
CMD ["/start.sh"]

EXPOSE 80 443
