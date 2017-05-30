
CREATE TABLE `offices` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`city` VARCHAR(255) NULL DEFAULT NULL,
	`state` VARCHAR(255) NULL DEFAULT NULL,
	`key` VARCHAR(255) NULL DEFAULT NULL,
	`skypeChatId` VARCHAR(255) NULL DEFAULT NULL,
	`enabled` TINYINT(4) NULL DEFAULT NULL,
	`createdAt` DATETIME NULL DEFAULT NULL,
	`modifiedAt` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `key` (`key`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;


ALTER TABLE `players`
	ADD COLUMN `officeId` INT(11) NULL DEFAULT NULL AFTER `id`;
ALTER TABLE `players`
	ADD CONSTRAINT `fk_players_offices` FOREIGN KEY (`officeId`) REFERENCES `offices` (`id`);

ALTER TABLE `isms`
	ADD COLUMN `officeId` INT(11) NULL DEFAULT NULL AFTER `id`;
ALTER TABLE `isms`
	ADD CONSTRAINT `fk_isms_offices` FOREIGN KEY (`officeId`) REFERENCES `offices` (`id`);


ALTER TABLE `matches`
	ADD COLUMN `officeId` INT(11) NULL DEFAULT NULL AFTER `id`;
ALTER TABLE `matches`
	ADD CONSTRAINT `fk_matches_offices` FOREIGN KEY (`officeId`) REFERENCES `offices` (`id`);


INSERT INTO `offices` (`id`, `city`, `state`, `key`, `skypeChatId`, `enabled`, `createdAt`, `modifiedAt`)
VALUES (1, 'Ames', 'Iowa', '6ca60c6a-c103-4884-8d84-6444cec51939', '8:brettmeyerxpx', '1', NOW(), NOW());

UPDATE `players`
SET `officeId` = 1;

UPDATE `matches`
SET `officeId` = 1;

UPDATE `isms`
SET `officeId` = 1;
