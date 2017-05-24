
CREATE TABLE `offices` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`city` VARCHAR(255) NULL DEFAULT NULL,
	`state` VARCHAR(255) NULL DEFAULT NULL,
	`hash` VARCHAR(255) NULL DEFAULT NULL,
	`skypeChatId` VARCHAR(255) NULL DEFAULT NULL,
	`enabled` TINYINT(4) NULL DEFAULT NULL,
	`createdAt` DATETIME NULL DEFAULT NULL,
	`modifiedAt` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `hash` (`hash`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;