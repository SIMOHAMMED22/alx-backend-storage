--SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
--that computes and store the average weighted score for a student.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_score DECIMAL(10,2);
    DECLARE total_weight DECIMAL(10,2);
    DECLARE avg_weighted_score DECIMAL(10,2);

    SELECT SUM(score * weight) INTO total_score, SUM(weight) INTO total_weight
    FROM scores
    WHERE user_id = user_id;

    IF total_weight > 0 THEN
        SET avg_weighted_score = total_score / total_weight;
    ELSE
        SET avg_weighted_score = 0;
    END IF;

    INSERT INTO average_weighted_scores (user_id, average_score)
    VALUES (user_id, avg_weighted_score);
END //
DELIMITER ;
