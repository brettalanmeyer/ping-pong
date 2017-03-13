
CREATE TABLE `teams_players` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`teamId` INT(11) NULL DEFAULT NULL,
	`playerId` INT(11) NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	INDEX `fk_teams_players_teams` (`teamId`),
	INDEX `fk_teams_players_players` (`playerId`),
	CONSTRAINT `fk_teams_players_players` FOREIGN KEY (`playerId`) REFERENCES `players` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `fk_teams_players_teams` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
