-- script that creates a table users following these requirements
-- id, email, name, and country

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  country ENUM('US', 'CO', 'TN') DEFAULT 'US'
);
