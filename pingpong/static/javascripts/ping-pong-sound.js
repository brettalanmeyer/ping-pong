function PingPongSound(){

	this.audioFiles = [];
	this.index = 0;

	for(var i in arguments){
		this.audioFiles.push("/static/audio/" + arguments[i]);
	}
	shuffle(this.audioFiles);

	this.play = function(playSound){
		if(playSound == undefined){
			playSound = true;
		}

		if(playSound && this.audioFiles.length > 0){
			var audio = new Audio(this.audioFiles[this.index % this.audioFiles.length]);
			audio.currentTime = 0;
			audio.play();
			this.index++;
		}
	}
}
