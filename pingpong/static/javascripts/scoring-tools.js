$(function(){

	var scoringTools = $("#scoring-tools");

	if(scoringTools.exists()){

		scoringTools.find("button[data-action=score], button[data-action=undo]").on("click", function(){
			var button = $(this);
			$.post("/buttons/" + button.data("color") + "/" + button.data("action"));
		});

		scoringTools.find(".random-score").on("click", function(){
			scoringTools.find("button[data-action=score]").eq(randRange(0, 3)).click();
		});

		scoringTools.find(".random-undo").on("click", function(){
			scoringTools.find("button[data-action=undo]").eq(randRange(0, 3)).click();
		});

		var scoringToolsInterval = null;

		scoringTools.find(".auto-score").on("click", function(){
			if(scoringToolsInterval == null){
				scoringToolsInterval = setInterval(function(){
					scoringTools.find("button[data-action=score]").eq(randRange(0, 3)).click();
				}, 100);
			} else {
				clearInterval(scoringToolsInterval)
				scoringToolsInterval = null;
			}
		});

	}

});
