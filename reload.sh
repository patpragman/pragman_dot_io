#!/bin/bash

# fetch changes

git pull
git merge master/origin

echo "reloading web application, GIT PUSH RECEIVED!"
touch /var/www/test_pragman_io_wsgi.py