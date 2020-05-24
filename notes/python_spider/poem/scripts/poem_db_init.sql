-- 创建数据库
CREATE DATABASE IF NOT EXISTS poem CHARSET=utf8;

-- 创建数据表
CREATE TABLE IF NOT EXISTS `poem_collections`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `category_first` VARCHAR(100) NOT NULL,
   `category_second` VARCHAR(100) NOT NULL,
   `poem_name` VARCHAR(800) NOT NULL,
   `poet` VARCHAR(40) NOT NULL,
   `content` VARCHAR(65535) NOT NULL,
   PRIMARY KEY ( `id` )
) DEFAULT CHARSET=utf8;