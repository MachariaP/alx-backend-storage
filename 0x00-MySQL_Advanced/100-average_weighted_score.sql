-- Create a stored procedure to compute and store the average weighted score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE weighted_score_sum FLOAT DEFAULT 0;
    DECLARE final_score FLOAT;

    -- Calculate the sum of weighted scores
    SELECT SUM(score * weight) INTO weighted_score_sum
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate the total weight
    SELECT SUM(weight) INTO total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate the final weighted average score
    SET final_score = IF(total_weight > 0, weighted_score_sum / total_weight, 0);

    -- Update the user's average score
    UPDATE users SET average_score = final_score WHERE id = user_id;
END$$
DELIMITER ;
