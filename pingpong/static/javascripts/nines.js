$(function(){

	var nines = $("#nines");

	if(nines.exists()){

		var matchId = nines.data("matchid");

		var socket = io.connect();
		socket.on("response", update);

		var colors = ["green", "yellow", "blue", "red"];
		var playerNames = {};
		var scores = {};
		var boards = {};

		for(var i = 0; i < colors.length; i++){
			var color = colors[i];

			playerNames[color] = $("[data-color=" + color + "][data-var=name");
			scores[color] = $("[data-color=" + color + "][data-var=score");
			boards[color] = $("[data-color=" + color + "][data-var=board");
		}

		function update(data){
			if(data == null) return;

			if(data.redirect){
				window.location = "/matches/" + data.matchId
			}

			if(data.matchId != matchId) return;

			if(data.complete){
				$("#play-again").removeClass("hidden");
				$("#undo").removeClass("hidden");
			}

			for(var i = 0; i < colors.length; i++){
				var color = colors[i];

				var previousScore = parseInt(scores[color].html());
				var nextScore = data.players[color].points;

				playerNames[color].html(data.players[color].playerName);
				scores[color].html(data.players[color].points);
				boards[color].toggleClass("out", data.players[color].out);

				if(previousScore != nextScore){
					playerNames[color].addClass("scored");
				}
			}
			setTimeout(function(){
				for(var i in colors){
					var color = colors[i];
					playerNames[color].removeClass("scored");
				}
			}, 2000);
		}
	}

});
