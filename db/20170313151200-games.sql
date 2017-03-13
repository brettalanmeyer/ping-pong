
CREATE TABLE `games` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`matchId` INT(11) NULL DEFAULT NULL,
	`game` INT(11) NULL DEFAULT NULL,
	`green` INT(11) NULL DEFAULT NULL,
	`yellow` INT(11) NULL DEFAULT NULL,
	`blue` INT(11) NULL DEFAULT NULL,
	`red` INT(11) NULL DEFAULT NULL,
	`winner` INT(11) NULL DEFAULT NULL,
	`winnerScore` INT(11) NULL DEFAULT NULL,
	`loser` INT(11) NULL DEFAULT NULL,
	`loserScore` INT(11) NULL DEFAULT NULL,
	`createdAt` DATETIME NULL DEFAULT NULL,
	`modifiedAt` DATETIME NULL DEFAULT NULL,
	`completedAt` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	INDEX `fk_games_matches` (`matchId`),
	INDEX `fk_games_winner` (`winner`),
	INDEX `fk_games_loser` (`loser`),
	INDEX `fk_games_green_players` (`green`),
	INDEX `fk_games_yellow_players` (`yellow`),
	INDEX `fk_games_blue_players` (`blue`),
	INDEX `fk_games_red_players` (`red`),
	CONSTRAINT `fk_games_blue_players` FOREIGN KEY (`blue`) REFERENCES `players` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `fk_games_green_players` FOREIGN KEY (`green`) REFERENCES `players` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `fk_games_loser` FOREIGN KEY (`loser`) REFERENCES `teams` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `fk_games_matches` FOREIGN KEY (`matchId`) REFERENCES `matches` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `fk_games_red_players` FOREIGN KEY (`red`) REFERENCES `players` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `fk_games_winner` FOREIGN KEY (`winner`) REFERENCES `teams` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `fk_games_yellow_players` FOREIGN KEY (`yellow`) REFERENCES `players` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
