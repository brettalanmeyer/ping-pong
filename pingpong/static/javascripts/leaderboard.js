$(function(){

	$(".table-sortable").stupidtable();


	var sort = hashManager.get("sort");
	var dir = hashManager.get("dir");

	if(sort != null && dir != null){
		$("#leaderboard, .opponent-table").each(function(){
			$(this).find("th[data-label=" + sort + "]").stupidsort(dir);
		});
	} else {
		$("#leaderboard.singles").find("th.elo").stupidsort("desc");
		$("#leaderboard.doubles").find("th.win-percentage").stupidsort("desc");
		$("#leaderboard.nines").find("th.win-percentage").stupidsort("desc");
	}


	var headers = $("#leaderboard, .opponent-table").find("thead").find("th");

	$("#leaderboard").bind("aftertablesort", function(event, data){
		var i = 1;
		$(this).find("tbody").find("tr").each(function(){
			$(this).find("td:first").html(i++);
		});
	});

	$("#leaderboard, .opponent-table").bind("aftertablesort", function(event, data){
		var header = headers.eq(data.column);
		hashManager.set("sort", header.data("label"));
		hashManager.set("dir", data.direction);
	});


	$(".leaderboard-player-container .nav-tabs li").on("click", function(){
		$(".leaderboard-player-container .nav-tabs li").removeClass("active");

		var source = $(this);
		setTab(source.data("matchtype"));

		hashManager.set("match-type", source.data("matchtype"));
	});

	function setTab(matchType){
		$("li[data-matchtype=" + matchType + "]").addClass("active");
		$(".leaderboard-player-container .opponent-table").addClass("hidden");
		$(".leaderboard-player-container .opponent-table[data-matchtype=" + matchType + "]").removeClass("hidden");
	}

	var matchType = hashManager.get("match-type");
	if(matchType != null){
		setTab(matchType);
	} else {
		setTab("singles");
	}

	$("#leaderboard, .opponent-table").each(function(){

		var rows = $(this).find("tbody").find("tr");
		var row = hashManager.get("row");

		if(row != null){
			rows.filter("[data-id=" + row + "]").addClass("active");
		}

		rows.on("click", function(){
			var source = $(this);

			if(source.hasClass("active")){
				source.removeClass("active");
				hashManager.set("row", null);
			} else {
				rows.removeClass("active");
				source.addClass("active");
				hashManager.set("row", source.data("id"));
			}

		});

	});

});
