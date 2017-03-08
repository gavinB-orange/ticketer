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
