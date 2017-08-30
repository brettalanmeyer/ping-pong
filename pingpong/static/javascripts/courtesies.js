$(function(){

	if($("#courtesies").exists()){

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
