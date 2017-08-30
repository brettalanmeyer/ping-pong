function PingPongSound(){

	this.audioFiles = [];
	this.index = 0;

	for(var i in arguments){
		var audio = new Audio("/static/audio/" + arguments[i]);
		audio.load();
		this.audioFiles.push(audio);
	}
	shuffle(this.audioFiles);

	this.play = function(playSound){
		if(playSound == undefined){
			playSound = true;
		}

		if(playSound && this.audioFiles.length > 0){
			var audio = this.audioFiles[this.index % this.audioFiles.length];
			audio.currentTime = 0;
			audio.play();
			this.index++;
		}
	}
}

