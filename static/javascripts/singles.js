$(function(){

	if($("#singles").length > 0){

		var socket = io.connect();
		socket.on("response", update);

		var set = $("[data-var=set");
		var yellowName = $("[data-color=yellow][data-var=name");
		var yellowScore = $("[data-color=yellow][data-var=score");
		var yellowServing = $("[data-color=yellow][data-var=serving");

		var greenName = $("[data-color=green][data-var=name");
		var greenScore = $("[data-color=green][data-var=score");
		var greenServing = $("[data-color=green][data-var=serving");

		var singlesAudio = new Audio("/static/audio/multi-player-start.wav").play();
		var scoreAudio = new Audio("/static/audio/coin.wav");
		var undoAudio = new Audio("/static/audio/picking-up.wav");

		function update(data){
			if(data == null) return;
			if(data.matchType != "singles") return;

			set.html(data.game);

			yellowName.html(data.teams.yellow.playerName);
			greenName.html(data.teams.green.playerName);

			yellowServing.removeClass("active");
			greenServing.removeClass("active");

			var isScore = false;
			var isUndo = false;

			if(data.teams.yellow.points > parseInt(yellowScore.html()) || data.teams.green.points > parseInt(greenScore.html())){
				isScore = true;
			} else if(data.teams.yellow.points < parseInt(yellowScore.html()) || data.teams.green.points < parseInt(greenScore.html())){
				isUndo = true;
			}

			if(isScore){
				scoreAudio.currentTime = 0;
				scoreAudio.play();
			} else if(isUndo){
				undoAudio.currentTime = 0;
				undoAudio.play();
			}

			yellowScore.html(pad(data.teams.yellow.points));
			greenScore.html(pad(data.teams.green.points));

			if(data.teams.yellow.serving){
				yellowServing.addClass("active");
			} else if(data.teams.green.serving){
				greenServing.addClass("active");
			}

			for(var color in data.teams){
				var team = data.teams[color];

				var cells = $("tr[data-teamid=" + team.teamId + "]").find("td");
				cells.eq(0).html(team.playerName);

				for(var i = 0; i < team.games.length; i++){
					var game = team.games[i];

					if(game.score != null){
						cells.eq(i + 1).html(pad(game.score));
						if(game.win){
							cells.eq(i + 1).addClass("win");
						}
					}
				}
			}

			sayings(data.teams.yellow.points, data.teams.green.points);

			if(data.complete){
				if(data.teams.green.winner){
					teamId = data.teams.green.teamId;
				} else if(data.teams.yellow.winner){
					teamId = data.teams.yellow.teamId;
				}

				if(data.teams.green.winner || data.teams.yellow.winner){
					$("tr[data-teamid=" + teamId + "]").find("td").first().append(" - <strong>Winner!</strong>");
				}
			}
		}

	}

});