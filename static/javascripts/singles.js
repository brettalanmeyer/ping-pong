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

		function update(data){
			if(data == null) return;

			set.html(data.game);

			yellowName.html(data.teams.yellow.playerName);
			yellowScore.html(pad(data.teams.yellow.points));

			greenName.html(data.teams.green.playerName);
			greenScore.html(pad(data.teams.green.points));

			yellowServing.removeClass("active");
			greenServing.removeClass("active");

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
				} else {
					teamId = data.teams.yellow.teamId;
				}

				$("tr[data-teamid=" + teamId + "]").find("td").first().append(" - <strong>Winner!</strong>");
			}
		}

	}

});