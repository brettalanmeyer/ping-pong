$(function(){

	if($("#nines").length > 0){

		var socket = io.connect();
		socket.on("response", update);

		var colors = ["green", "yellow", "blue", "red"];
		var playerNames = {};
		var scores = {};

		for(var i = 0; i < colors.length; i++){
			var color = colors[i];

			playerNames[color] = $("[data-color=" + color + "][data-var=name");
			scores[color] = $("[data-color=" + color + "][data-var=score");
		}

		function update(data){

			for(var i = 0; i < colors.length; i++){
				var color = colors[i];

				playerNames[color].html(data.players[color].playerName);
				scores[color].html(data.players[color].points);
			}
		}
	}

});
