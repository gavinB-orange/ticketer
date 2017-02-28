#!/bin/bash

# create a database using a docker container with known user/password
# and accessible from the host machine.

PASSWORD_FILE=$(pwd)/db.pass

# create a random (numeric only) password
read rstuff < /dev/urandom
echo $rstuff | od -b | head -1 | awk '{print $2$3$4$5$6$7$8$9$10}' > $PASSWORD_FILE

docker run --name ticketerdb -e MYSQL_ROOT_PASSWORD=$(cat $PASSWORD_FILE)\
                             -e MYSQL_DATABASE=TICKETER\
                             -e MYSQL_USER=ticketer\
                             -e MYSQL_PASSWORD=$(cat $PASSWORD_FILE)\
                             -e MYSQL_ROOT_HOST=172.17.0.1\
                             -p 6603:3306 -d mysql/mysql-server:latest

echo "`date` : waiting for the container to boot"
while ! nc -z 172.17.0.1 6603; do
    sleep 10
    echo -n "."
done
echo "`date` : waiting over - continuing"

# create the user table in the database
mysql -uticketer -p$(cat $PASSWORD_FILE) --host=172.17.0.1 --port=6603 -DTICKETER -e 'CREATE TABLE `TICKETER`.`tbl_user` (\
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
mysql -uroot -p$(cat $PASSWORD_FILE) --host=172.17.0.1 --port=6603 -DTICKETER < script.sql


echo "Database can now be accessed via :"
echo "mysql -uticketer -p$(cat $PASSWORD_FILE) --host=172.17.0.1 --port=6603 -DTICKETER"
