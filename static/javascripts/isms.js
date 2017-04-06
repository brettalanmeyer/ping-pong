var isms = [];
var ismContainer;

function sayings(left, right){
	shuffle(isms);

	for(var i = 0; i < isms.length; i++){
		ism = isms[i];

		if(ism.left == left && ism.right == right){
			if(ism.saying.length > 25){
				ismContainer.addClass("long");
			}

			ismContainer.html(ism.saying);
			ismContainer.stop(true, true).fadeIn("slow").delay(2000).fadeOut("slow").removeClass("long");
			break;
		}
	}
}

$(function(){

	if($("#singles").length > 0 || $("#doubles").length > 0){

		ismContainer = $("<div />").addClass("ism-container").html("Jet Fuel Can't Melt Steel Beamz");
		$("body").append(ismContainer);

		if(isms.length == 0){
			$.get("/isms.json").done(function(data){
				isms = data;
			});
		}

	}

});
