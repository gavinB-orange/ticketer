#!/bin/bash

# create a database using a docker container with known user/password
# and accessible from the host machine.

PASSWORD_FILE=$(pwd)/db.pass

read rstuff < /dev/urandom
echo $rstuff | od -c | head -1 | awk '{print $2$3$4$5$6$7$8$9$10}' > $PASSWORD_FILE

docker run --name ticketerdb -e MYSQL_ROOT_PASSWORD=$(cat $PASSWORD_FILE)\
                             -e MYSQL_DATABASE=TICKETER\
                             -e MYSQL_USER=ticketer\
                             -e MYSQL_PASSWORD=$(cat $PASSWORD_FILE)\
                             -e MYSQL_ROOT_HOST=172.17.0.1\
                             -p 6603:3306 -d mysql/mysql-server:latest

echo "Database can now be accessed via :"
echo "mysql -uticketer -p$(cat $PASSWORD_FILE) --host=172.17.0.1 --port=6603 -DTICKETER"
