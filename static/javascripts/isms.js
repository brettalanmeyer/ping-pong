var saying;

function sayings(left, right){
	shuffle(isms);

	for(var i = 0; i < isms.length; i++){
		ism = isms[i];

		console.log(ism.left == left && ism.right == right);
		if(ism.left == left && ism.right == right){

			saying.html(ism.saying).animate({ opacity: 1 }, 1000);

			setTimeout(function(){
				saying.animate({ opacity: 0 }, 1000);
			}, 2500);

			return;
		}
	}
}

$(function(){
	saying = $("#saying");
});
