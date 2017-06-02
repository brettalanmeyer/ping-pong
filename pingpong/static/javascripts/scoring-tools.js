$(function(){

	var scoringTools = $("#scoring-tools");
	var playAgain = $("#play-again");
	var scoringToolsInterval = null;

	if(scoringTools.exists()){

		scoringTools.find("button[data-color]").on("click", function(){
			$.post($(this).data("action"), { "key": scoringTools.data("key") }).done(complete);
		});

		scoringTools.find(".random-score").on("click", function(){
			scoringTools.find("button.score").eq(randRange(0, 3)).click();
		});

		scoringTools.find(".random-undo").on("click", function(){
			scoringTools.find("button.undo").eq(randRange(0, 3)).click();
		});

		scoringTools.find(".auto-score").on("click", function(){
			if(scoringToolsInterval == null){
				scoringToolsInterval = setInterval(function(){
					scoringTools.find("button.score").eq(randRange(0, 3)).click();
				}, 150);
			} else {
				clearInterval(scoringToolsInterval);
				scoringToolsInterval = null;
			}
		});

	}

	function complete(){
		if(playAgain.is(":visible")){
			clearInterval(scoringToolsInterval)
		}
	}

});
