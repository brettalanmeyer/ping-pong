CREATE TABLE `courtesies` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`officeId` INT(11) NULL DEFAULT NULL,
	`text` VARCHAR(255) NULL DEFAULT NULL,
	`file` VARCHAR(255) NULL DEFAULT NULL,
	`approved` TINYINT(4) NULL DEFAULT NULL,
	`createdAt` DATETIME NULL DEFAULT NULL,
	`modifiedAt` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	INDEX `fk_courtesies_offices` (`officeId`),
	CONSTRAINT `fk_courtesies_offices` FOREIGN KEY (`officeId`) REFERENCES `offices` (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
