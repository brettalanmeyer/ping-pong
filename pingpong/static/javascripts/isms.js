var isms = [];
var ismContainer;

function sayings(left, right){
	shuffle(isms);

	for(var i = 0; i < isms.length; i++){
		ism = isms[i];

		if(ism.left == left && ism.right == right){
			displaySaying(ism.saying);
			break;
		}
	}
}

function displaySaying(message){
	if(message.length > 25){
		ismContainer.addClass("long");
	}

	ismContainer.html(message);
	ismContainer.stop(true, true).fadeIn("slow").delay(4000).fadeOut("slow").removeClass("long");
}

$(function(){

	if($("#singles").exists() || $("#doubles").exists() || $("#nines").exists()){

		ismContainer = $("<div />").addClass("ism-container");
		$("body").append(ismContainer);

		if(isms.length == 0){
			$.get("/isms.json").done(function(data){
				isms = data;
			});
		}

	}

});
