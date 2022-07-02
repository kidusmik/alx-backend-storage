-- script that creates a stored procedure AddBonus
-- that adds a new correction for a student

DROP PROCEDURE IF EXISTS AddBonus;

DELIMITER $$

CREATE PROCEDURE AddBonus(user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
  DECLARE new_name VARCHAR(255);
  DECLARE new_id INT DEFAULT 0;

  SELECT name INTO new_name FROM projects
  WHERE name = project_name;

  IF new_name IS NULL THEN
    INSERT INTO projects(name) VALUES(project_name);
  END IF;

  SELECT id INTO new_id FROM projects
  WHERE name = project_name;

  INSERT INTO corrections(user_id, project_id, score)
  VALUES (user_id, new_id, score);
END $$
DELIMITER ;
