var isms = [];
var ismContainer;
var ismQueue = [];
var ismInProgress = false;

function sayings(left, right){
	shuffle(isms);

	for(var i = 0; i < isms.length; i++){
		ism = isms[i];

		if(ism.left == left && ism.right == right){
			addToSayingQueue(ism.saying, false);
			break;
		}
	}
}

function addToSayingQueue(message, isImage){
	ismQueue.unshift({
		message: message,
		isImage: isImage
	});
	displaySaying();
}

function displaySaying(){

	if(ismInProgress || ismQueue.length == 0){
		return;
	}

	var data = ismQueue.pop();
	var message = data.message;
	var isImage = data.isImage;

	ismContainer.removeClass("image very-long long medium short small");

	if(isImage){
		ismContainer.addClass("image");
		message = $("<img />").attr("src", message);
	} else if(message.length > 500){
		ismContainer.addClass("very-long");
	} else if(message.length > 400){
		ismContainer.addClass("long");
	} else if(message.length > 300){
		ismContainer.addClass("medium");
	} else if(message.length > 200){
		ismContainer.addClass("short");
	} else if(message.length > 100){
		ismContainer.addClass("small");
	}

	ismInProgress = true;
	ismContainer.html(message);
	ismContainer.stop(true, true).fadeIn("slow").delay(4000).fadeOut("slow", function(){
		setTimeout(function(){
			ismInProgress = false;
			displaySaying();
		}, 50);
	});
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
