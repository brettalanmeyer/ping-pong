$(function(){

	var nines = $("#nines");

	if(nines.exists()){

		var matchId = nines.data("matchid");
		var office = $("meta[name=office]").attr("content");
		var disconnected = false;

		var socket = io.connect(domain());
		socket.on("response-" + office, update);
		socket.on("smack-talk-" + office, smackTalk);
		socket.on("disconnect", function(){
			if(!disconnected){
				setTimeout(function(){
					location.reload();
				}, 500);
			}
		});
		$(window).on("beforeunload", function(){
			disconnected = true;
			socket.close();
		});

		var scoreAudio = new PingPongSound(
			"boing.wav",
			"bump.wav",
			"picking-up.wav",
			"coin.wav",
			"spring-jump.wav",
			"pacman-chomp.wav"
		);

		var courtesyAudio = new PingPongSound(
			"courtesy01.mp3",
			"courtesy02.mp3",
			"courtesy03.mp3",
			"courtesy04.mp3",
			"courtesy05.mp3",
			"courtesy06.mp3",
			"courtesy07.mp3",
			"courtesy08.mp3",
			"courtesy09.mp3",
			"courtesy10.mp3"
		);

		var colors = ["green", "yellow", "blue", "red"];
		var playerNames = {};
		var scores = {};
		var boards = {};
		var avatars = {};

		for(var i = 0; i < colors.length; i++){
			var color = colors[i];

			playerNames[color] = $("[data-color=" + color + "][data-var=name");
			scores[color] = $("[data-color=" + color + "][data-var=score");
			boards[color] = $("[data-color=" + color + "][data-var=board");
			avatars[color] = $(".avatar-nines." + color);
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

			var playScore = false;
			var playCourtesy = false;

			for(var i = 0; i < colors.length; i++){
				var color = colors[i];

				var previousScore = parseInt(scores[color].html());
				var nextScore = data.players[color].points;

				playerNames[color].html(data.players[color].playerName);
				scores[color].html(data.players[color].points);
				boards[color].toggleClass("out", data.players[color].out);

				if(previousScore != nextScore){
					playerNames[color].addClass("scored");

					playCourtesy = (nextScore == 1);
					playScore = !playCourtesy;
				}

				if(data.players[color].playerAvatar){
					src = "/players/" + data.players[color].playerId + "/avatar/" + data.players[color].playerAvatar;

					if(avatars[color].attr("src") != src){
						avatars[color].attr("src", src);
					}
				} else {
					avatars[color].attr("src", "/static/images/silhouette-" + randRange(1, 7) + ".png");
				}
			}

			setTimeout(function(){
				for(var i in colors){
					var color = colors[i];
					playerNames[color].removeClass("scored");
				}
			}, 2000);

			scoreAudio.play(playScore);
			courtesyAudio.play(playCourtesy);
		}

		enableUndo();

	}

});
