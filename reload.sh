#!/bin/bash

# fetch changes

git reset --hard
git pull origin master

echo "reloading web application, GIT PUSH RECEIVED!"
touch /var/www/test_pragman_io_wsgi.py