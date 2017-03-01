#!/bin/bash

# create a database using a docker container with known user/password
# and accessible from the host machine.

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
mysql_extras=$(pwd)/mysql_extra_options
echo "[client]" > $mysql_extras
echo "password = $pass" >> $mysql_extras
chmod 600 $mysql_extras

echo "`date` : waiting for the container to boot"
while ! nc -z 172.17.0.1 6603; do
    sleep 10
    echo -n "."
done
echo "`date` : waiting over - continuing"

# create the user table in the database
mysql --defaults-extra-file=$mysql_extras --host=172.17.0.1 --port=6603 -DTICKETER -uticketer -e 'CREATE TABLE `TICKETER`.`tbl_user` (\
`user_id` BIGINT NOT NULL AUTO_INCREMENT,\
`user_name` VARCHAR(64) NULL,\
`user_username` VARCHAR(64) NULL,\
`user_password` VARCHAR(256) NULL,\
`user_role` VARCHAR(8) NULL,\
PRIMARY KEY (`user_id`));'
# add the stored procedure for creating users - note requires root priviledges
cat > script.sql<<'EOF'
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(64),
    IN p_username VARCHAR(64),
    IN p_password VARCHAR(256),
    IN p_role VARCHAR(8)
)
BEGIN
    IF ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN
        select "Username Exists !!";
    ELSE
        insert into tbl_user
        (
            user_name,
            user_username,
            user_password,
            user_role
        )
        values
        (
            p_name,
            p_username,
            p_password,
            p_role
        );
    END IF;
END$$
DELIMITER ;
EOF
mysql --defaults-extra-file=$mysql_extras --host=172.17.0.1 --port=6603 -DTICKETER -uroot < script.sql
# add the stored procedure for validating users - note requires root privileges
cat > script.sql<<'EOF'
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(64)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;
EOF
mysql --defaults-extra-file=$mysql_extras --host=172.17.0.1 --port=6603 -DTICKETER -uroot < script.sql


echo "Database can now be accessed via :"
echo "mysql --defaults-extra-file=$mysql_extras --host=172.17.0.1 --port=6603 -DTICKETER -uticketer"
