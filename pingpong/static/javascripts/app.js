$(function(){

	$(".table-sortable").stupidtable();

	$("#leaderboard").find("th.elo").stupidsort("desc");

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

	$("#matches-player-filter").on("change", function(){
		var playerId = $(this).val();
		if(playerId.length == 0){
			window.location = "/matches";
		} else {
			window.location = "/matches/players/" + playerId;
		}
	});

	$(".alert-dismissible").each(function(){
		var source = $(this);

		if(source.hasClass("auto-close")){
			setTimeout(function(){
				source.fadeOut();
			}, 2000);
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

function shuffle(a) {
	for (let i = a.length; i; i--) {
		let j = Math.floor(Math.random() * i);
		[a[i - 1], a[j]] = [a[j], a[i - 1]];
	}
}

function pad(num){
	return ("00" + num).substr(-2,2);
}
