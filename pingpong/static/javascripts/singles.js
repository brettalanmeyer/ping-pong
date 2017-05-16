$(function(){

	var singles = $("#singles");

	if(singles.exists()){

		var matchId = singles.data("matchid");

		var socket = io.connect();
		socket.on("response", update);

		var set = $("[data-var=set");
		var colors = ["green", "yellow"];

		var names = {
			green: $("[data-color=green][data-var=nam]e"),
			yellow: $("[data-color=yellow][data-var=name]")
		};

		var serving = {
			green: $("[data-color=green][data-var=serving]"),
			yellow: $("[data-color=yellow][data-var=serving]")
		};

		var scores = {
			green: $("[data-color=green][data-var=score]"),
			yellow: $("[data-color=yellow][data-var=score]")
		};

		var avatars = {
			green: $(".avatar-singles.green"),
			yellow: $(".avatar-singles.yellow")
		};

		var elo = {
			green: $("[data-color=green][data-var=elo]"),
			yellow: $("[data-color=yellow][data-var=elo]")
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
				cells.eq(0).html('<a href="/leaderboard/players/' + data.teams[color].playerId + '">' + data.teams[color].playerName + '</a>');

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
					src = "/players/" + team.playerId + "/avatar/" + team.playerAvatar;

					if(avatars[color].attr("src") != src){
						avatars[color].attr("src", src);
					}
				} else {
					avatars[color].attr("src", "/static/images/silhouette-" + randRange(1, 7) + ".png");
				}

				if(team.elo != null){
					elo[color].html(parseInt(Math.round(team.elo.current)));
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
