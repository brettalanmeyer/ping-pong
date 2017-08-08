function PingPongSound(){
	this.audioFiles = [];

	for(var i in arguments){
		this.audioFiles.push(new Audio("/static/audio/" + arguments[i]));
	}

	this.play = function(playSound){
		if(playSound == undefined){
			playSound = true;
		}

		if(playSound){
			var i = randRange(0, this.audioFiles.length - 1);
			this.audioFiles[i].currentTime = 0;
			this.audioFiles[i].play();
		}
	}

}
