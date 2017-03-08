DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createTicket`(
IN p_key VARCHAR(64),
IN p_summary VARCHAR(256),
IN p_owner_id BIGINT
)
BEGIN
    insert into tickets
    (
        ticket_key,
        ticket_summary,
        ticket_owner
    )
    values
    (
        p_key,
        p_summary,
        p_owner
    );
END$$
DELIMITER ;

