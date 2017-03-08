$(function(){

	var index = -1;
	var inputs = $("#players-form").find("input");
	var buttons = $(".color-button");
	var playerList = $(".player-list")
	var players = $(".player");
	var play = $("#players-form-play");
	var redo = $("#players-form-redo");
	var randomize = $("#players-form-randomize");

	next();

	function next(){
		buttons.removeClass("active");

		if(index == inputs.length - 1){
			playerList.hide();
			play.show();
			randomize.show();
		} else {
			index++;
			buttons.eq(index).addClass("active");
			var input = inputs.eq(index);
		}
	}

	players.on("click", function(){
		var source = $(this);
		inputs.eq(index).val(source.data("id"));
		buttons.eq(index).html(source.html());
		source.hide();
		next();
	});

	redo.on("click", function(){
		buttons.html("");
		inputs.val("");
		playerList.show();
		players.show();
		play.hide();
		index = -1;
		next();
	});

	randomize.on("click", function(){

		var values = $.map(inputs, function(input){
			return $(input).val();
		});

		shuffle(values);

		for(i in values){
			inputs.eq(i).val(values[i]);
			buttons.eq(i).html(players.filter("[data-id=" + values[i] + "]").html());
		}

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