CREATE TABLE `TICKETER`.`tickets` (\
`ticket_id` BIGINT NOT NULL AUTO_INCREMENT,\
`ticket_key` VARCHAR(64) NULL,\
`ticket_summary` VARCHAR(256) NULL,\
`ticket_owner` BIGINT,\
`ticket_content_id` BIGINT NULL,\
PRIMARY KEY (`ticket_id`));

