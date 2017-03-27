from flask import Flask
from utils import database
from models import MatchModel, TeamModel, GameModel, PlayerModel, ScoreModel
from datetime import datetime
from  sqlalchemy.sql.expression import func
import random, math

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
session = database.setupSession(app)


def createMatch():

	if random.randrange(0,2) == 0:
		matchType = "singles"
	else:
		matchType = "doubles"

	match = MatchModel.MatchModel(matchType, 1, True, False, datetime.now(), datetime.now())
	match.playTo = 21
	match.numOfGames = [1,3,5][random.randrange(0,3)]

	session.add(match)
	session.commit()

	return match

def createTeam(matchId):
	team = TeamModel.TeamModel(matchId, datetime.now(), datetime.now())
	session.add(team)
	session.commit()

	return team

def createGames(match):
	for i in range(0, match.numOfGames):
		green = match.teams[1 if i % 2 == 0 else 0].players[0].id
		yellow = match.teams[1 if i % 2 == 1 else 0].players[0].id

		game = GameModel.GameModel(match.id, i + 1, green, yellow, None, None, datetime.now(), datetime.now())
		session.add(game)
		session.commit()

def scoring(match):

	gamesNeededToWinMatch = int(math.ceil(float(match.numOfGames) / 2.0))

	team1Wins = 0
	team2Wins = 0

	for i in range(0, match.numOfGames):
		match.game = i + 1
		session.commit()

		winner, winnerScore, loser, loserScore = score(match)
		match.games[i].winner = winner.id
		match.games[i].winnerScore = winnerScore
		match.games[i].loser = loser.id
		match.games[i].loserScore = loserScore
		match.games[i].completedAt = datetime.now()
		session.commit()

		if winner.id == match.teams[0].id:
			team1Wins += 1
		if winner.id == match.teams[1].id:
			team2Wins += 1

		if team1Wins == gamesNeededToWinMatch or team2Wins == gamesNeededToWinMatch:
			match.complete = True
			match.completedAt = datetime.now()

			if team1Wins:
				index1 = 0
				index2 = 1
			else:
				index1 = 1
				index2 = 0

			match.teams[index1].win = True
			match.teams[index1].loss = False
			match.teams[index1].modifiedAt = datetime.now()

			match.teams[index2].win = False
			match.teams[index2].loss = True
			match.teams[index2].modifiedAt = datetime.now()

			session.commit()
			break

def score(match):

	team1 = match.teams[0]
	team2 = match.teams[1]

	team1Points = 0
	team2Points = 0

	while True:
		if random.randrange(0,2) == 0:
			teamId = team1.id
			team1Points += 1
		else:
			teamId = team2.id
			team2Points += 1

		score = ScoreModel.ScoreModel(match.id, teamId, match.game, datetime.now())
		session.add(score)
		session.commit()

		team1Win = team1Points >= match.playTo and team1Points >= team2Points + 2
		team2Win = team2Points >= match.playTo and team2Points >= team1Points + 2

		if team1Win:
			return team1, team1Points, team2, team2Points
		elif team2Win:
			return team2, team2Points, team1, team1Points

def generate():
	players = session.query(PlayerModel.PlayerModel).order_by(func.rand()).limit(4)

	match = createMatch()

	team1 = createTeam(match.id)
	team2 = createTeam(match.id)

	player1 = None
	player2 = None
	player3 = None
	player4 = None

	for player in players:
		if player1 == None:
			player1 = player
		elif player2 == None:
			player2 = player
		elif player3 == None:
			player3 = player
		elif player4 == None:
			player4 = player

	team1.players.append(player1)
	team2.players.append(player2)

	if match.matchType == "doubles":
		team1.players.append(player3)
		team2.players.append(player4)

	session.commit()

	createGames(match)

	scoring(match)

def main():
	session.query(MatchModel.MatchModel).delete()

	for i in range(0, 100):
		print("Generating match #:" + str(i + 1))
		generate()

if __name__ == "__main__":
	main()