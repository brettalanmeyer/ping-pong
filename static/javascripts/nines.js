$(function(){

	if($("#nines").length > 0){

		var socket = io.connect();
		socket.on("response", update);

		var colors = ["green", "yellow", "blue", "red"];
		var playerNames = {};
		var scores = {};
		var boards = {};

		var ninesAudio = new Audio("/static/audio/multi-player-start.wav").play();
		var scoreAudio = new Audio("/static/audio/bump.wav");
		var undoAudio = new Audio("/static/audio/coin.wav");

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

			var isScore = false;
			var isUndo = false;

			for(var i = 0; i < colors.length; i++){
				var color = colors[i];

				var previousScore = parseInt(scores[color].html());
				var nextScore = data.players[color].points;

				if(nextScore > previousScore){
					isScore = true;
				} else if(nextScore < previousScore){
					isUndo = true;
				}

				playerNames[color].html(data.players[color].playerName);
				scores[color].html(data.players[color].points);
				boards[color].toggleClass("out", data.players[color].out);
			}

			if(isScore){
				scoreAudio.currentTime = 0;
				scoreAudio.play();
			} else if(isUndo){
				undoAudio.currentTime = 0;
				undoAudio.play();
			}
		}
	}

});
