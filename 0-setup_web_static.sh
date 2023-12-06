#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "Holberton School" > /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

echo "server {
    location /hbnb_static {
            alias /data/web_static/current/;
            index index.htm index.html;
    }
}" > /etc/nginx/sites-available/default
sudo service nginx restart
exit 0
