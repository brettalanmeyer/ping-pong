$(function(){

	var singles = $("#singles");

	if(singles.exists()){

		var matchId = singles.data("matchid");

		var socket = io.connect();
		socket.on("response", update);

		var set = $("[data-var=set");
		var colors = ["green", "yellow"];

		var names = {
			green: $("[data-color=green][data-var=name"),
			yellow: $("[data-color=yellow][data-var=name")
		};

		var serving = {
			green: $("[data-color=green][data-var=serving"),
			yellow: $("[data-color=yellow][data-var=serving")
		};

		var scores = {
			green: $("[data-color=green][data-var=score"),
			yellow: $("[data-color=yellow][data-var=score")
		};

		function update(data){
			if(data == null) return;
			if(data.matchId != matchId) return;

			set.html(data.game);

			for(var i in colors){
				var color = colors[i];

				names[color].html(data.teams[color].playerName);
				if(data.teams[color].serving){
					serving[color].addClass("active");
				} else {
					serving[color].removeClass("active");
				}

				var previousScore = parseInt(scores[color].html());
				var nextScore = parseInt(data.teams[color].points);

				scores[color].html(pad(data.teams[color].points));
				if(previousScore != nextScore){
					scores[color].parent(".score-board").addClass("scored");
				}
			}
			setTimeout(function(){
				for(var i in colors){
					var color = colors[i];
					scores[color].parent(".score-board").removeClass("scored");
				}
			}, 2000);

			for(var color in data.teams){
				var team = data.teams[color];

				var cells = $("tr[data-teamid=" + team.teamId + "]").find("td");
				cells.eq(0).html(team.playerName);

				for(var i = 0; i < team.games.length; i++){
					var game = team.games[i];
					var cell = cells.eq(i + 1).html("").removeClass("win");

					if(game.score != null){
						cell.html(pad(game.score));
						if(game.win){
							cell.addClass("win");
						}
					}
				}

				if(team.playerAvatar){
					$(".avatar-singles." + color).attr("src", "/players/" + team.playerId + "/avatar/" + team.playerAvatar);
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

				$(".complete-hide").addClass("hidden");
				$(".complete-show").removeClass("hidden");
			}

		}

		enableUndo();

	}

});