$(function(){

	if($("#isms").length > 0){

		$("button.play-ism").on("click", function(){

			var source = $(this);
			var icon = source.find(".glyphicon")
			icon.removeClass("glyphicon-play").addClass("glyphicon-pause");

			var audio = source.find("audio")[0];
			audio.play();

			audio.onended = function(){
				icon.removeClass("glyphicon-pause").addClass("glyphicon-play");
			};
		});

	}

});


function sayings(left, right){
	shuffle(isms);

	for(var i = 0; i < isms.length; i++){
		ism = isms[i];

		if(ism.left == left && ism.right == right){
			var sound = new Audio("/static/isms/" + ism.file);
			sound.play();
			break;
		}
	}
}