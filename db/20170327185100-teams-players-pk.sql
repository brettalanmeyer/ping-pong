
ALTER TABLE `teams_players`
	DROP COLUMN `id`;

ALTER TABLE teams_players ADD PRIMARY KEY(teamId, playerId);
