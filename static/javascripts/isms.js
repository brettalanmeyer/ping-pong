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

