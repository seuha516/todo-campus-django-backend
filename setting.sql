CREATE SCHEMA `todocampus_db` DEFAULT CHARACTER SET utf8mb4;
use todocampus_db;

create user 'todocampus_user'@'%' identified by 'qdted7Z6Q!';
grant all privileges on todocampus_db.* to 'todocampus_user'@'%';
FLUSH PRIVILEGES;

CREATE TABLE `account` (
  `username` VARCHAR(12) NOT NULL,
  `hashedPassword` VARCHAR(255) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `nickname` VARCHAR(8) NOT NULL UNIQUE,
  `setting` JSON NULL,
  `notice` JSON NULL,
  PRIMARY KEY (`username`));

CREATE TABLE `weektable` (
  `num` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(12) NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `color` CHAR(10) NULL,
  `etc` VARCHAR(255) NULL,
  `credit` INT NULL,
  `professor` VARCHAR(20) NULL,
  `time` JSON NULL
);
ALTER TABLE weektable
	ADD CONSTRAINT
	FOREIGN KEY(username) REFERENCES account(username)
	ON UPDATE CASCADE
	ON DELETE CASCADE;

CREATE TABLE `calendar` (
  `num` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(12) NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `color` CHAR(10) NULL,
  `content` VARCHAR(255) NULL,
  `location` VARCHAR(30) NULL,
  `start` DATETIME NOT NULL,
  `end` DATETIME NOT NULL
);
ALTER TABLE calendar
	ADD CONSTRAINT
	FOREIGN KEY(username) REFERENCES account(username)
	ON UPDATE CASCADE
	ON DELETE CASCADE;

CREATE TABLE `post` (
  `num` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(12) NOT NULL,
  `nickname` VARCHAR(8) NOT NULL,
  `title` VARCHAR(30) NOT NULL,
  `body` text NULL,
  `image` json NULL,
  `tag` json NULL,
  `comment` json NULL,
  `like` json NULL,
  `publishedDate` datetime NULL,
  `lastModifiedDate` datetime NULL
);
ALTER TABLE post
	ADD CONSTRAINT
	FOREIGN KEY(username) REFERENCES account(username)
	ON UPDATE CASCADE
	ON DELETE CASCADE;

CREATE TABLE `memo` (
  `num` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(12) NOT NULL,
  `body` text NULL
);
ALTER TABLE memo
	ADD CONSTRAINT
	FOREIGN KEY(username) REFERENCES account(username)
	ON UPDATE CASCADE
	ON DELETE CASCADE;

CREATE TABLE `todo` (
  `num` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(12) NOT NULL,
  `title` VARCHAR(30) NOT NULL,
  `category` VARCHAR(8) NULL,
  `noted` INT NULL,
  `due` datetime NULL
);
ALTER TABLE memo
	ADD CONSTRAINT
	FOREIGN KEY(username) REFERENCES account(username)
	ON UPDATE CASCADE
	ON DELETE CASCADE;