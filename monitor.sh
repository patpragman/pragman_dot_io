#!/bin/bash
# much thank to stack overflow for this one - not exactly sexy, but should work for my purposes.

changed=0
git remote update && git status -uno | grep -q 'Your branch is behind' && changed=1
if [ $changed = 1 ]; then
    git pull
    touch /var/www/test_pragman_io_wsgi.py
    echo "Updated successfully";
else
    echo "Up-to-date"
fi