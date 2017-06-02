from BaseTest import BaseTest
from pingpong.services.MatchService import MatchService
from pingpong.services.ScoreService import ScoreService
from pingpong.services.TeamService import TeamService
import json

matchService = MatchService()
scoreService = ScoreService()
teamService = TeamService()

class TestScoreService(BaseTest):

	def createMatch(self, officeId):
		return matchService.create(officeId, "singles")

	def createTeam(self, officeId):
		match = self.createMatch(officeId)
		return teamService.create(match.id)

	def createScore(self, officeId):
		team = self.createTeam(officeId)
		return scoreService.score(team.match.id, team.id, team.match.game)

	def test_select(self):
		office = self.office()

		with self.ctx:
			score = self.createScore(office["id"])
			scores = scoreService.select()
			assert scores.count() > 0

	def test_selectCount(self):
		office = self.office()

		with self.ctx:
			score = self.createScore(office["id"])
			scores = scoreService.select()
			count = scoreService.selectCount()
			assert scores.count() == count

	def test_selectById(self):
		office = self.office()

		with self.ctx:
			score = self.createScore(office["id"])
			selected = scoreService.selectById(score.id)
			assert score == selected

	def test_selectByMatch(self):
		office = self.office()

		with self.ctx:
			score = self.createScore(office["id"])
			scores = scoreService.selectByMatch(score.match)
			assert scores.count() == 1
			assert scores.first() == score

	def test_selectByMatchId(self):
		office = self.office()

		with self.ctx:
			score = self.createScore(office["id"])
			scores = scoreService.selectByMatchId(score.match.id)
			assert scores.count() == 1
			assert scores.first() == score

	def test_selectLastScoreByMatchId(self):
		office = self.office()

		with self.ctx:
			score1 = self.createScore(office["id"])
			matchId = score1.matchId
			teamId = score1.teamId
			game = score1.match.game

			score2 = scoreService.score(matchId, teamId, game)
			score3 = scoreService.score(matchId, teamId, game)
			score4 = scoreService.score(matchId, teamId, game)

			lastScore = scoreService.selectLastScoreByMatchId(matchId)
			assert lastScore == score4

	def test_delete(self):
		office = self.office()

		with self.ctx:
			score = self.createScore(office["id"])
			scoreService.delete(score)
			deletedScore = scoreService.selectById(score.id)
			assert deletedScore == None

	def test_getScore(self):
		office = self.office()

		with self.ctx:
			score1 = self.createScore(office["id"])
			matchId = score1.matchId
			teamId = score1.teamId
			game = score1.match.game

			for i in range(0,9):
				scoreService.score(matchId, teamId, game)

			scores = scoreService.getScore(matchId, teamId, game)
			assert scores == 10

	def test_deleteByMatch(self):
		office = self.office()

		with self.ctx:
			score1 = self.createScore(office["id"])
			matchId = score1.matchId
			teamId = score1.teamId
			game = score1.match.game

			for i in range(0,9):
				scoreService.score(matchId, teamId, game)

			scoreService.deleteByMatchId(matchId)
			scores = scoreService.selectByMatchId(matchId)
			assert scores.count() == 0

	def test_serialize(self):
		office = self.office()

		with self.ctx:
			score = self.createScore(office["id"])
			scores = scoreService.selectByMatchId(score.matchId)
			data = json.loads(scoreService.serialize(scores))
			assert len(data) == scores.count()
