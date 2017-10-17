
ALTER TABLE `matches`
	ADD COLUMN `matchNum` INT(11) NULL DEFAULT NULL AFTER `complete`;

UPDATE `matches`
SET `matchNum` = 1;
