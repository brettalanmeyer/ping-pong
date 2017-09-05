
ALTER TABLE `courtesies`
	ADD COLUMN `language` VARCHAR(255) NULL DEFAULT NULL AFTER `text`,
	ADD COLUMN `slow` TINYINT(4) NULL DEFAULT NULL AFTER `language`;

UPDATE `courtesies`
SET `slow` = 0;

UPDATE `courtesies`
SET `language` = 'en-us';