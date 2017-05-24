$(function(){

	var scoringTools = $("#scoring-tools");

	if(scoringTools.exists()){

		scoringTools.find("button[data-color]").on("click", function(){
			$.post($(this).data("action"));
		});

		scoringTools.find(".random-score").on("click", function(){
			scoringTools.find("button.score").eq(randRange(0, 3)).click();
		});

		scoringTools.find(".random-undo").on("click", function(){
			scoringTools.find("button.undo").eq(randRange(0, 3)).click();
		});

		var scoringToolsInterval = null;

		scoringTools.find(".auto-score").on("click", function(){
			if(scoringToolsInterval == null){
				scoringToolsInterval = setInterval(function(){
					scoringTools.find("button.score").eq(randRange(0, 3)).click();
				}, 100);
			} else {
				clearInterval(scoringToolsInterval)
				scoringToolsInterval = null;
			}
		});

	}

});
