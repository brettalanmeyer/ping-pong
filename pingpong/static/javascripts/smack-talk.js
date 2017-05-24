$(function(){

	var smackTalk = $("#smack-talk");

	if(smackTalk.exists()){

		var smackTalkForm = $("#smack-talk-form");
		var smackTalkInput = $("#smack-talk-input");
		var smackTalkButton = $("#smack-talk-button");

		smackTalkForm.on("submit", function(){
			$.post(smackTalkForm.attr("action"), { message: smackTalkInput.val() });
			hideSmackTalkInput();
			return false;
		});

		smackTalkButton.on("click", function(){
			disableUndo();
			smackTalkButton.hide();
			smackTalkForm.show();
			smackTalkInput.focus();
		});

		smackTalkInput.on("keydown", function(e){
			if(e.which == 27){
				hideSmackTalkInput();
			}
		});

		function hideSmackTalkInput(){
			smackTalkButton.show();
			smackTalkForm.hide();
			smackTalkInput.val("");
		}

	}

});

function smackTalk(data){
	displaySaying(data.message);
}
