-- Create an index on the first letter of the name column
ALTER TABLE names ADD INDEX idx_name_first (name(1));
