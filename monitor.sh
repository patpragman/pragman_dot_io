#!/bin/bash

cd /home/ciegoservices/test


changed=0
git remote update && git status -uno | grep -q 'Your branch is behind' && changed=1
if [ $changed = 1 ]; then
    # pull down the current hotness
    git reset --hard
    git pull origin master

    echo "reloading web application, doing the hourly check"
    touch /var/www/test_pragman_io_wsgi.py
else
    echo "Git repo is up to date..."
fi