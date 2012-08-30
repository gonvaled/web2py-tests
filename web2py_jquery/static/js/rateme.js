$(document).ready(function() {
	// generate markup
	var ratingMarkup = ["Please rate: "];
	for(var i=1; i <= 5; i++) {
		ratingMarkup[ratingMarkup.length] = "<a href='#'>" + i + "</a> ";
	}
	var container = $("#rating");
	// add markup to container
	container.html(ratingMarkup.join(''));

    var url = "rateme";

	// add click handlers
	container.find("a").click(function(e) {
		e.preventDefault();
		// send requests
		$.post(url, {rating: $(this).html()}, function(xml) {
			// format result
			var result = [
				"Thanks for rating, current average: ",
				$("average", xml).text(),
				", number of votes: ",
				$("count", xml).text()
			];
			// output result
			$("#rating").html(result.join(''));
		} );
	});
});
