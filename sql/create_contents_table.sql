CREATE TABLE `TICKETER`.`ticket_contents` (
`content_id` BIGINT NOT NULL AUTO_INCREMENT,
`ticket_id` BIGINT,
`comment_author_id` BIGINT,
`next_content_id` BIGINT NULL,
`text` VARCHAR(1024),
PRIMARY KEY (`content_id`));

