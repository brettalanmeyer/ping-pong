$(function(){

	if($("#nines").length > 0){

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
			if(data.matchType != "nines") return;

			if(data.redirect){
				window.location = "/matches/" + data.matchId
			}

			if(data.complete){
				$("#play-again").removeClass("hidden");
			}

			for(var i = 0; i < colors.length; i++){
				var color = colors[i];

				playerNames[color].html(data.players[color].playerName);
				scores[color].html(data.players[color].points);
				boards[color].toggleClass("out", data.players[color].out);
			}

		}
	}

});
