
ALTER TABLE `teams_players`
	DROP COLUMN `id`;

ALTER TABLE teams_players ADD PRIMARY KEY(teamId, playerId);

UPDATE teams t1
LEFT JOIN matches m1 ON t1.matchId = m1.id
SET t1.win = (
	SELECT IF(COUNT(s1.id) < 9, 1, 0) as win
	FROM scores s1
	WHERE s1.teamId = t1.id
),
t1.loss = (
	SELECT IF(COUNT(s2.id) = 9, 1, 0) as loss
	FROM scores s2
	WHERE s2.teamId = t1.id
)
WHERE m1.matchType = 'nines';
