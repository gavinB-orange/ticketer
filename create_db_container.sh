#!/bin/bash

# create a database using a docker container with known user/password
# and accessible from the host machine.
#

set -eu

# create a random (numeric only) password
read rstuff < /dev/urandom
pass=$(echo $rstuff | od -b | head -1 | awk '{print $2$3$4$5$6$7$8$9$10}')

docker run --name ticketerdb -e MYSQL_ROOT_PASSWORD=$pass\
                             -e MYSQL_DATABASE=TICKETER\
                             -e MYSQL_USER=ticketer\
                             -e MYSQL_PASSWORD=$pass\
                             -e MYSQL_ROOT_HOST=172.17.0.1\
                             -p 6603:3306 -d mysql/mysql-server:latest

# create mysql option file
mysql_defaults=$(pwd)/mysql_extra_options
echo "[client]" > $mysql_defaults
echo "password = $pass" >> $mysql_defaults
chmod 600 $mysql_defaults

echo "`date` : waiting for the container to boot"
while ! nc -z 172.17.0.1 6603; do
    sleep 10
    echo -n "."
done
echo "`date` : waiting over - continuing"

# create the user table in the database
mysql --defaults-file=$mysql_defaults --host=172.17.0.1 --port=6603 -DTICKETER -uticketer < sql/create_user_table.sql
# add the stored procedure for creating users - note sp requires root priviledges
mysql --defaults-file=$mysql_defaults --host=172.17.0.1 --port=6603 -DTICKETER -uroot < sql/create_sp_createuser.sql
# add the stored procedure for validating users - note sp requires root privileges
mysql --defaults-file=$mysql_defaults --host=172.17.0.1 --port=6603 -DTICKETER -uroot < sql/create_sp_validatelogin.sql
# create the tickets table in the database
mysql --defaults-file=$mysql_defaults --host=172.17.0.1 --port=6603 -DTICKETER -uticketer < sql/create_tickets_table.sql
# tickets have one or more comments
mysql --defaults-file=$mysql_defaults --host=172.17.0.1 --port=6603 -DTICKETER -uticketer < sql/create_contents_table.sql
# add the stored procedure for validating users - note sp requires root privileges
mysql --defaults-file=$mysql_defaults --host=172.17.0.1 --port=6603 -DTICKETER -uroot < sql/create_sp_createticket.sql


echo "Database can now be accessed via :"
echo "mysql --defaults-file=$mysql_defaults --host=172.17.0.1 --port=6603 -DTICKETER -uticketer"
