
CREATE TABLE `scores` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`matchId` INT(11) NULL DEFAULT NULL,
	`teamId` INT(11) NULL DEFAULT NULL,
	`game` INT(11) NULL DEFAULT NULL,
	`createdAt` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	INDEX `fk_scores_matches` (`matchId`),
	INDEX `fk_scores_teams` (`teamId`),
	CONSTRAINT `fk_scores_matches` FOREIGN KEY (`matchId`) REFERENCES `matches` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `fk_scores_teams` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
