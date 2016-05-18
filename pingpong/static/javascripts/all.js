$(function(){

	$(".value-picker").each(function(){
		var source = $(this);

		var input = source.find(".input");
		var up = source.find(".up");
		var down = source.find(".down");

		var value = data("value");
		var min = data("min");
		var max = data("max");
		var interval = data("interval");

		up.on("click", function(){
			enable();
			value += interval;
			if(value >= max){
				value = max;
				up.addClass("disabled");
			}
			update();
			return false;
		});

		down.on("click", function(){
			enable();
			value -= interval;
			if(value <= min){
				value = min;
				down.addClass("disabled");
			}
			update();
			return false;
		});

		function data(attribute){
			return parseInt(source.data(attribute));
		}

		function update(){
			input.val(value).trigger("change");
		}

		function enable(){
			up.removeClass("disabled");
			down.removeClass("disabled");
		}

	});



	$(".player-picker").each(function(){
		var source = $(this);
		var players = source.find(".team-player");
		var gameId = source.data("gameid");
		var index = 0;

		players.first().addClass("current");

		$(".player-select").on("click", function(){
			var player = $(this);
			var teamPlayer = $(players[index]);

			var data = {
				gameId: gameId,
				teamId: teamPlayer.data("teamid"),
				playerId: player.data("playerid")
			};

			$.post("/games/" + gameId + "/players/", data, function(){

				teamPlayer.removeClass("current").find(".name").html(player.html());
				player.remove();
				index++;

				if(index >= players.length){
					$(".players-list").remove();
					$(".select-score").removeClass("hidden");
				} else {
					$(players[index]).addClass("current");
				}

			});

		});

	});


	$(".games-play").each(function(){

		var source = $(this);
		var gameId = source.data("gameid");
		var playTo = parseInt(source.data("playto"));

		var inputs = source.find(".input");

		inputs.on("change", function(){
			var input = $(this);
			var data = {
				teamId: input.data("teamid"),
				score: input.val()
			};
			$.post("/games/" + gameId + "/play/score/", data, function(){

				if(input.val() >= playTo){
					alert("You Win!");
					$.post("/games/" + gameId + "/play/complete/");
				}
			});
		});

	});

});
