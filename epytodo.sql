CREATE DATABASE IF NOT EXISTS epytodo;
USE epytodo;

CREATE TABLE IF NOT EXISTS user
(
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	password VARCHAR(512) NOT NULL
);

CREATE TABLE IF NOT EXISTS task
(
    task_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	begin TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	end TIMESTAMP DEFAULT 0,
	status INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_has_task
(
    fk_user_id INT NOT NULL,
	fk_task_id INT NOT NULL
);