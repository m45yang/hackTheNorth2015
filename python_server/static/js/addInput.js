$(document).ready(function() {
	$("#searchSubmit").on('click', function (event) {
		event.preventDefault();

		$("#resultText").fadeOut();
		$("#result").fadeOut();
		$(this).text('Loading...');

		var searchName = $('input[name="searchName"]').val();
		if ($('input[name="reddit"]').is(":checked")) {
			var reddit = 1;
		} else {
			reddit = 0;
		}

		if ($('input[name="twitter"]').is(":checked")) {
			var twitter = 1;
		} else {
			twitter = 0;
		}

		$.ajax({
			url: "/search",
			type: "post",
			data: {
				searchName : searchName,
				reddit : reddit,
				twitter : twitter
			},
			success: function(result) {
				$("#resultText").fadeIn();
				$("#result").html(result.score);
				$("#result").fadeIn();
				// var bottomList = '<p>Bottom three comments/tweets: ' + result.tb[0] + ' ' + result.tb[1] + ' ' + result.tb[2] + '</p>';
				// var topList = '<p>Top three comments/tweets: ' + result.tb[3] + ' ' + result.tb[4] + ' ' + result.tb[5] + '</p>';
				// $("#topAndBottom").html(bottomList + topList);
				$("#searchSubmit").text('Sentimentalize!');
			}
		});
	});
});

