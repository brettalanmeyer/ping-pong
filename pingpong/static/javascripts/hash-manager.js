
var hashManager = new function(){

	var hash;
	var items = {};

	this.init = function(){
		hash = window.location.hash.substring(1);
		parse();
	};

	this.set = function(key, value){
		if(value != null && value != undefined && (typeof value != "string" || typeof value == "string" && value.length > 0)){
			items[key] = value;
		} else if(key in items){
			delete items[key];
		}
		update();
	};

	this.get = function(key){
		if(key in items){
			return items[key];
		}

		return null;
	}

	function update(){
		var list = [];
		for(key in items){
			list.push(key + "=" + items[key]);
		}
		hash = list.join("&");
		window.location.hash = hash;
	}

	function parse(){
		if(hash.length == 0){
			return;
		}

		pairs = hash.split("&");

		for(var i = 0; i < pairs.length; i++){
			pair = pairs[i].split("=");
			var key = pair[0];
			var value = pair[1];

			items[key] = value;
		}
	}

};

$(document).ready(hashManager.init);
