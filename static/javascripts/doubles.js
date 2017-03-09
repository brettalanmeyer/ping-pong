$(function(){

	if($("#doubles").length > 0){

		var socket = io.connect();
		socket.on("response", update);

		var set = $("[data-var=set");

		var colors = ["green", "yellow", "blue", "red"];
		var teams = ["north", "south"];

		var playerNames = {
			green: $("[data-color=green][data-var=name"),
			yellow: $("[data-color=yellow][data-var=name"),
			blue: $("[data-color=blue][data-var=name"),
			red: $("[data-color=red][data-var=name")
		};

		var serving = {
			green: $("[data-color=green][data-var=serving"),
			yellow: $("[data-color=yellow][data-var=serving"),
			blue: $("[data-color=blue][data-var=serving"),
			red: $("[data-color=red][data-var=serving")
		};

		var scores = {
			north: $("[data-team=north][data-var=score"),
			south: $("[data-team=south][data-var=score")
		};

		function update(data){
			if(data == null) return;

			set.html(data.game);

			for(var i in colors){
				var color = colors[i];
				playerNames[color].html(data.players[color].playerName);

				if(data.players[color].serving){
					serving[color].addClass("active");
				} else {
					serving[color].removeClass("active");
				}
			}

			for(var i in teams){
				var team = teams[i];
				scores[team].html(pad(data.teams[team].points));
			}

			for(var side in data.teams){
				var team = data.teams[side];

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

			sayings(data.teams.south.points, data.teams.north.points);

			if(data.complete){
				if(data.teams.north.winner){
					teamId = data.teams.north.teamId;
				} else {
					teamId = data.teams.south.teamId;
				}

				$("tr[data-teamid=" + teamId + "]").find("td").first().append(" - <strong>Winner!</strong>");
			}
		}

	}

});
