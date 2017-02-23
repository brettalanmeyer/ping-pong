$(function(){

	var index = -1;
	var inputs = $("#players-form").find("input");
	var buttons = $(".color-button");
	var playerList = $(".player-list")
	var players = $(".player");
	var play = $("#players-form-play");
	var redo = $("#players-form-redo");

	next();

	function next(){
		buttons.removeClass("active");

		if(index == inputs.length - 1){
			playerList.hide();
			play.show();
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



});
