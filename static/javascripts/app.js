$(function(){

	if($("#player-selector").length > 0){

		var index = -1;
		var inputs = $("#players-form").find("input");
		var names = $(".player-table .name");
		var playerList = $(".player-list")
		var players = $(".player");
		var play = $("#players-form-play");
		var redo = $("#players-form-redo");
		var randomize = $("#players-form-randomize");
		var selectSound = new Audio("/static/audio/picking-up.wav");
		var randomizeSound = new Audio("/static/audio/down-the-flagpole.wav");
		var redoSound = new Audio("/static/audio/bowser-fails.wav");


		new Audio("/static/audio/boing.wav").play();

		next();

		function next(){
			names.removeClass("active");

			if(index == inputs.length - 1){
				playerList.hide();
				play.show();
				randomize.show();
			} else {
				index++;
				names.eq(index).addClass("active");
				var input = inputs.eq(index);
			}
		}

		players.on("click", function(){
			var source = $(this);
			inputs.eq(index).val(source.data("id"));
			names.eq(index).html(source.html());

			source.hide();
			next();

			selectSound.play();
		});

		redo.on("click", function(){
			names.html("");
			inputs.val("");
			playerList.show();
			players.show();
			play.hide();
			index = -1;
			next();

			redoSound.play();
		});

		randomize.on("click", function(){

			var values = $.map(inputs, function(input){
				return $(input).val();
			});

			shuffle(values);

			for(i in values){
				inputs.eq(i).val(values[i]);
				names.eq(i).html(players.filter("[data-id=" + values[i] + "]").html());
			}

			randomizeSound.play();
		});
	}

	$("#leaderboard").stupidtable();

	if($("#matches-new").length > 0){
		new Audio("/static/audio/bonus-game-match.wav").play();
	}

	if($("#matches-play-to").length > 0){
		new Audio("/static/audio/hit-while-flying.wav").play();
	}

	if($("#matches-num-of-games").length > 0){
		new Audio("/static/audio/spring-jump.wav").play();
	}

	$("form.action-delete").on("submit", function(){
		return confirm("Are you sure you want to delete this?");
	});

});

function shuffle(a) {
	for (let i = a.length; i; i--) {
		let j = Math.floor(Math.random() * i);
		[a[i - 1], a[j]] = [a[j], a[i - 1]];
	}
}

function pad(num){
	return ("00" + num).substr(-2,2);
}