function PingPongSound(){

	this.audioFiles = [];

	for(var i in arguments){
		var audio = new Audio("/static/audio/" + arguments[i]);
		audio.load();
		this.audioFiles.push(audio);
	}

	this.play = function(playSound){
		if(playSound == undefined){
			playSound = true;
		}

		if(playSound && this.audioFiles.length > 0){
			var index = randRange(0, this.audioFiles.length - 1);
			var audio = this.audioFiles[index];
			audio.currentTime = 0;
			audio.play();
		}
	}
}
