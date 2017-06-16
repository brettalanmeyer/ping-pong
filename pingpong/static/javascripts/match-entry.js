$(function(){

	if($("#match-entry").exists()){

		var matchTypeValue;
		var matchType = $("input[name=matchType]");
		var numOfGames = $("input[name=numOfGames]").prop("disabled", true);
		var players = $("input[name=playerId]").prop("disabled", true);
		var button = $("button").prop("disabled", true);
		var enablePlayers = true;

		matchType.on("change", function(){
			var source = $(this);

			matchTypeValue = source.val();

			numOfGames.prop("checked", false);
			numOfGames.prop("disabled", source.val() == "nines");
			players.prop("disabled", true).prop("checked", false);
			enablePlayers = true;

			if(source.val() == "nines"){
				players.prop("disabled", false);
			}
		});

		numOfGames.on("change", function(){
			if(enablePlayers){
				players.prop("disabled", false);
				enablePlayers = false;
			}
			buildSets();
		});

		players.on("change", function(){
			var limit = 4;
			var numChecked = players.filter(":checked").length;

			if(matchTypeValue == "singles"){
				limit = 2;
			}

			if(numChecked == limit){
				players.filter(":not(:checked)").prop("disabled", true);
			} else {
				players.prop("disabled", false);
			}

			buildSets();
		});

		var cell = $('<td><input type="text" name=""></td>');
		var sets = $(".set-sets");
		var team1 = $(".set-team1");
		var team2 = $(".set-team2");

		function buildSets(){
			var num = parseInt(numOfGames.filter(":checked").val());

			sets.html("");
			team1.html("");
			team2.html("");

			var numSelected = players.filter(":checked").length;
			var team1name = players.filter(":checked").first().data("name");
			var team2name = players.filter(":checked").last().data("name");

			if(numSelected == 2 || numSelected == 4){
				for(var i = 0; i <= num; i++){
					if(i == 0){
						sets.append(cell.clone().html(""));
						team1.append(cell.clone().html(team1name));
						team2.append(cell.clone().html(team2name));
					} else {
						sets.append(cell.clone().html(i));

						var cell1 = cell.clone();
						cell1.find("input").attr("name", "set-" + i);
						team1.append(cell1);

						var cell2 = cell.clone();
						cell2.find("input").attr("name", "set-" + i);
						team2.append(cell2);
					}
				}

				button.prop("disabled", false);
			} else {
				button.prop("disabled", true);
			}
		}
	}

});
