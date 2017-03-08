CREATE TABLE `TICKETER`.`tbl_user` (
`user_id` BIGINT NOT NULL AUTO_INCREMENT,
`user_name` VARCHAR(64) NULL,
`user_username` VARCHAR(64) NULL,
`user_password` VARCHAR(256) NULL,
`user_role` VARCHAR(8) NULL,
PRIMARY KEY (`user_id`));
