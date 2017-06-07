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
	ismContainer.removeClass("very-long long medium short small");

	if(message.length > 500){
		ismContainer.addClass("very-long");
	} else if(message.length > 400){
		ismContainer.addClass("long");
	} else if(message.length > 300){
		ismContainer.addClass("medium");
	} else if(message.length > 200){
		ismContainer.addClass("short");
	} else if(message.length > 100){
		console.log("small");
		ismContainer.addClass("small");
	}

	ismContainer.html(message);
	ismContainer.stop(true, true).fadeIn("slow").delay(4000).fadeOut("slow");
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
