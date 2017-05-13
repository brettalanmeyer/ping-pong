$(function(){

	$(".table-sortable").stupidtable();

	$("#leaderboard.singles").find("th.elo").stupidsort("desc");

	$("#leaderboard").bind("aftertablesort", function(event, data){
		var i = 1;
		$(this).find("tbody").find("tr").each(function(){
			$(this).find("td:first").html(i++);
		});
	});

	$(".leaderboard-player-container .nav-tabs li").on("click", function(){
		$(".leaderboard-player-container .nav-tabs li").removeClass("active");

		var source = $(this);
		source.addClass("active");

		$(".leaderboard-player-container .opponent-table").addClass("hidden");
		$(".leaderboard-player-container .opponent-table[data-matchtype=" + source.data("matchtype") + "]").removeClass("hidden");
	}).first().trigger("click");

	$("form.action-delete").on("submit", function(){
		return confirm("Are you sure you want to delete this?");
	});

	$("#season-filter").on("change", function(){
		$(this).parent("form").submit();
	});

	var playerFilter = $("#matches-player-filter").on("change", matchesfilters);
	var opponentFilter = $("#matches-opponent-filter").on("change", matchesfilters);
	var matchTypeFilter = $("#matches-match-type-filter").on("change", matchesfilters);
	var seasonFilter = $("#matches-season-filter").on("change", matchesfilters);
	function matchesfilters(){
		params = [];

		var playerId = playerFilter.val();
		var opponentId = opponentFilter.val();
		var matchType = matchTypeFilter.val();
		var season = seasonFilter.val();

		if(playerId.length){
			params.push("playerId=" + playerId);
		}

		if(opponentId.length){
			params.push("opponentId=" + opponentId);
		}

		if(matchType.length){
			params.push("matchType=" + matchType);
		}

		if(season.length){
			params.push("season=" + season);
		}

		window.location = "/matches" + (params.length ? "?" : "") + params.join("&");
	}

	$(".alert-dismissible").each(function(){
		var source = $(this);

		if(source.hasClass("auto-close")){
			setTimeout(function(){
				source.fadeOut();
			}, 3000);
		}

		source.find(".close").on("click", function(){
			source.fadeOut("fast");
		});
	});

	jQuery.fn.extend({
		exists: function(){
			return this.length > 0;
		}
	});

});

function enableUndo(){
	$(document).on("keypress", function(e){
		$.post("/buttons/green/undo");
	});
}

function shuffle(a) {
	for (let i = a.length; i; i--) {
		let j = Math.floor(Math.random() * i);
		[a[i - 1], a[j]] = [a[j], a[i - 1]];
	}
}

function pad(num){
	return ("00" + num).substr(-2,2);
}

function randRange(min, max){
	return Math.floor(Math.random() * (max - min + 1)) + min;
}
