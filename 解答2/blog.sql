

CREATE DATABASE IF NOT EXISTS `myblog`;

USE `myblog`;

CREATE TABLE IF NOT EXISTS `user_info`(
    uid INT(10) NOT NULL AUTO_INCREMENT,
    account VARCHAR(20) NOT NULL DEFAULT "",
    password VARCHAR(20) DEFAULT "",
    role TINYINT(4)  DEFAULT 0,
    create_time INT(10)  DEFAULT 0,
    PRIMARY KEY (uid),
    INDEX (account)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS `blog_info`(
    id INT(10) NOT NULL AUTO_INCREMENT,
    uid INT(10) DEFAULT 0,
    head VARCHAR(20) DEFAULT "",
    content VARCHAR(5000) DEFAULT "",
    article_url VARCHAR(20) DEFAULT "",
    edit_time INT(10) DEFAULT 0,
    status TINYINT(4) DEFAULT 0,
    PRIMARY KEY (id, uid),
    INDEX (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

REPLACE INTO `user_info` (account, password, role, create_time) VALUES ("admin", "admin", 1, UNIX_TIMESTAMP(NOW()));
REPLACE INTO `user_info` (account, password, role, create_time) VALUES ("general", "general", 2, UNIX_TIMESTAMP(NOW()));
