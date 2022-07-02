-- script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.
-- Note: An average score can be a decimal

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
  DECLARE tot_score INT DEFAULT 0;
  DECLARE pro_count INT DEFAULT 0;

  SELECT SUM(score) INTO tot_score FROM corrections
  WHERE corrections.user_id = user_id;

  SELECT COUNT(*) INTO pro_count FROM corrections
  WHERE corrections.user_id = user_id;

  UPDATE users
  SET users.average_score = IF(pro_count = 0, 0, tot_score / pro_count)

  WHERE users.id = user_id;
END //
