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

		var saying = $("#saying");

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

			for(var i = 0; i < data.games.length; i++){
				var game = data.games[i];

				var cells = $("tr[data-teamid=" + game.teamId + "]").find("td");

				cells.eq(0).html(game.name);

				for(var j = 0; j < game.games.length; j++){
					var g = game.games[j];
					cells.eq(j + 1).html(pad(g.score));

					if(g.win){
						cells.eq(j + 1).addClass("win");
					}
				}
			}

			sayings(data.teams.yellow.points, data.teams.green.points);

			if(data.complete){
				if(data.teams.green.winner){
					teamId = data.teams.green.id;
				} else {
					teamId = data.teams.yellow.id;
				}

				$("tr[data-teamid=" + teamId + "]").find("td").first().append(" - <strong>Winner!</strong>");
			}
		}


		function sayings(left, right){
			shuffle(isms);

			for(var i = 0; i < isms.length; i++){
				ism = isms[i];

				if(ism.left == left && ism.right == right){

					saying.html(ism.saying).animate({ opacity: 1 }, 1000);

					setTimeout(function(){
						saying.animate({ opacity: 0 }, 1000);
					}, 2500);

					return;
				}

			}

		}


	}

});