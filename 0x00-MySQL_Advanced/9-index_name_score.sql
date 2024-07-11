-- Create an index on the first letter of the name column and the score
ALTER TABLE names ADD INDEX idx_name_first_score (name(1), score);
