# pull down the latest info from the server
# merge it in

git pull origin master
git merge origin/master

# now reload webapp
touch /var/www/test_pragman_io_wsgi.py