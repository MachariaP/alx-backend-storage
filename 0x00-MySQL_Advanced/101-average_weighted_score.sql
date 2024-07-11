-- Create a stored procedure to compute and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Temporary table to hold the weighted scores and total weights for each user
    DROP TEMPORARY TABLE IF EXISTS TempUserScores;
    CREATE TEMPORARY TABLE TempUserScores (
        user_id INT,
        weighted_score_sum FLOAT,
        total_weight FLOAT
    );

    -- Calculate the sum of weighted scores and total weights for each user
    INSERT INTO TempUserScores (user_id, weighted_score_sum, total_weight)
    SELECT corrections.user_id, SUM(corrections.score * projects.weight) AS weighted_score_sum, SUM(projects.weight) AS total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    GROUP BY corrections.user_id;

    -- Update the users table with the calculated average scores
    UPDATE users
    JOIN TempUserScores ON users.id = TempUserScores.user_id
    SET users.average_score = CASE
        WHEN TempUserScores.total_weight > 0 THEN TempUserScores.weighted_score_sum / TempUserScores.total_weight
        ELSE 0
    END;
END$$
DELIMITER ;
