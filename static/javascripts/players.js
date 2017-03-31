$(function(){

	if($("#players").length > 0){

		var play = $("#players-form-play");
		var players = $(".player");
		var numOfPlayers = parseInt($("#numOfPlayers").val());
		var numOfTeams = parseInt($("#numOfTeams").val());

		var introSound = new Audio("/static/audio/boing.wav").play();
		var selectSound = new Audio("/static/audio/picking-up.wav");

		players.on("click", function(){
			var source = $(this);
			select(source);
			checkLimit();
			playSound();
			return false;
		});

		function select(source){
			source.toggleClass("active");
			source.find("input[type=checkbox]").attr("checked", source.hasClass("active"));
		}

		function checkLimit(){
			if(players.filter(".active").length >= numOfPlayers){
				players.not(".active").attr("disabled", true);
				play.removeClass("hidden");
			} else {
				players.attr("disabled", false);
				play.addClass("hidden");
			}
		}

		function playSound(){
			selectSound.currentTime = 0;
			selectSound.play();
		}

	}

});
