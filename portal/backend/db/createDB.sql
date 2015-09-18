SET foreign_key_checks = 0;
use modwatch_dev;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `username` VARCHAR(128) NOT NULL,
  `role` 	VARCHAR(45) NOT NULL,
  `password` VARCHAR(128) NOT NULL,
  `salt`    VARCHAR(128) NOT NULL,
  `name` 	VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `email` 	VARCHAR(45) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `lang` VARCHAR(20) NOT NULL DEFAULT "sv",
  `cookie_id` VARCHAR(100),
  `cookie_expire` TIMESTAMP NULL,
  PRIMARY KEY (`username`)
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) UNIQUE NOT NULL,
  `time` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `installations`;
CREATE TABLE `installations` (
  `serial_number` VARCHAR(128) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `model` VARCHAR(45) NOT NULL,
  `customer` INT,
  `time` DATETIME DEFAULT NULL,
  PRIMARY KEY (`serial_number`),
  CONSTRAINT `FK_installations_customer` FOREIGN KEY `FK_installation_customer` (`customer`)
        REFERENCES `customers` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `controllers`;
CREATE TABLE `controllers` (
  `installation` VARCHAR(128) NOT NULL,
  `name` varchar(50) NOT NULL,
  `ip` varchar(50) NOT NULL,
  `time` DATETIME DEFAULT NULL,
  PRIMARY KEY (`installation`, `ip`),
  CONSTRAINT `FK_controllers_installations` FOREIGN KEY `FK_controllers_installations` (`installation`)
        REFERENCES `installations` (`serial_number`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `name` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL DEFAULT 'value',
  `address` varchar(50) NOT NULL,
  `controller_ip` varchar(128) NOT NULL,
  `installation` VARCHAR(128) NOT NULL,
  `time` DATETIME DEFAULT '1970-01-01',
  `value` VARCHAR(50) DEFAULT '0',
  PRIMARY KEY (`controller_ip`, `installation`, `name`),
  CONSTRAINT `fk_tags_controller_ip_installation`
      FOREIGN KEY (`installation`, `controller_ip`)
	  REFERENCES `controllers` (`installation`, `ip`)
	  ON DELETE CASCADE
	  ON UPDATE CASCADE,
  INDEX `where` (`name` ASC, `controller_ip` ASC, `installation` ASC),
  INDEX `where_type` (`type` ASC, `controller_ip` ASC, `installation` ASC)
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `assignees`;
CREATE TABLE `assignees` (
    `user` varchar(128) NOT NULL,
    `customer` INT NOT NULL,
    PRIMARY KEY (`user`, `customer`),
    CONSTRAINT `fk_assignees_user`
        FOREIGN KEY (`user`)
        REFERENCES `users` (`username`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        CONSTRAINT `fk_assignees_customer`
        FOREIGN KEY (`customer`)
        REFERENCES `customers` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `setting_types`;
CREATE TABLE  `setting_types` (
  `setting_name` varchar(50) NOT NULL,
  `min_value` float NOT NULL,
  `max_value` float NOT NULL,
  `default_value` float NOT NULL,
  `role` enum('user','technician','admin') NOT NULL,
  `group` int(10) unsigned DEFAULT NULL,
  `type` varchar(50) NOT NULL DEFAULT 'int',
  PRIMARY KEY (`setting_name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `settings`;
CREATE  TABLE IF NOT EXISTS `settings` (
	`installation` VARCHAR(128) NOT NULL,
	`setting_name` VARCHAR(50) NOT NULL,
	`value` FLOAT NOT NULL,
	PRIMARY KEY (`installation`, `setting_name`),
	CONSTRAINT `fk_settings_setting_types`
		FOREIGN KEY (`setting_name`)
		REFERENCES `setting_types` (`setting_name`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
	CONSTRAINT `FK_settings_installations` FOREIGN KEY `FK_settings_installations` (`installation`)
        REFERENCES `installations` (`serial_number`)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
) ENGINE = InnoDB;

DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `value` VARCHAR(50) NOT NULL,
  `time` DATETIME NOT NULL,
  `installation` VARCHAR(50) NOT NULL,
  `controller_ip` VARCHAR(50) NOT NULL,
  `type` varchar(50) NOT NULL DEFAULT 'value',
  `address` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `FK_log_installation` FOREIGN KEY `FK_log_installation` (`installation`)
    REFERENCES `installations` (`serial_number`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_log_installation_controller` FOREIGN KEY `FK_log_installation_controller` (`installation`, `controller_ip`)
    REFERENCES `controllers` (`installation`, `ip`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    INDEX `time index` USING BTREE (`time` ASC),
    INDEX `where index` (`time` DESC, `installation` ASC, `controller_ip` ASC, `name` ASC),
    INDEX `where_installation_controller` (`installation` ASC, `controller_ip` ASC, `time` DESC),
    INDEX `in_optimize` (`installation` ASC, `controller_ip` ASC, `name` ASC)

)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `sync_queue`;
CREATE TABLE  `sync_queue` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `installation` varchar(100) NOT NULL,
  `table` varchar(100) NOT NULL,
  `method` varchar(100) NOT NULL,
  `data` TEXT NOT NULL,
  `prev` TEXT DEFAULT NULL,
  `last_sync_attempt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`installation`)
) ENGINE=InnoDB;

DELIMITER ///

CREATE TRIGGER log_trigger AFTER INSERT ON log
  FOR EACH ROW
  BEGIN
    UPDATE tags SET `time` = NEW.`time`, `value` = NEW.`value` WHERE `name` = NEW.`name` AND `installation` = NEW.`installation` AND `controller_ip` = NEW.`controller_ip`;
    UPDATE controllers SET `time` = NEW.`time` WHERE `installation` = NEW.`installation` AND `ip` = NEW.`controller_ip`;
    UPDATE installations SET `time` = NEW.`time` WHERE `serial_number` = NEW.`installation`;
  END;
///

DELIMITER ;


SET foreign_key_checks = 1;
