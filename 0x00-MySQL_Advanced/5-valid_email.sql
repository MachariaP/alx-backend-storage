-- Drops existing 'before_email_update' trigger to avoid conflicts.
DROP TRIGGER IF EXISTS reset_valid_email;
DELIMITER $$

-- Creates a new trigger to validate email updates in 'users' table.
-- Activates before an update, marking 'valid_email' as 0 if email changes.
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END $$
DELIMITER ;
