CREATE DATABASE IF NOT EXISTS epytodo;
USE epytodo;

CREATE TABLE user IF NOT EXISTS (
    user_id int NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    PRIMARY KEY (user_id)
);
CREATE TABLE task IF NOT EXISTS(
    task_id int NOT NULL AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    begin DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    end DATETIME DEFAULT NULL,
    status varchar(255) DEFAULT "not started",
    PRIMARY KEY (task_id)
);
CREATE TABLE user_has_task IF NOT EXISTS(
    fk_user_id int,
    fk_task_id int
);
