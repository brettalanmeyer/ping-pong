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
			value += interval;
			if(value > max){
				value = max;
			}
			update();
			return false;
		});

		down.on("click", function(){
			value -= interval;
			if(value < min){
				value = min;
			}
			update();
			return false;
		});

		function data(attribute){
			return parseInt(source.data(attribute));
		}

		function update(){
			input.val(value);
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
				team: teamPlayer.data("team"),
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

});
