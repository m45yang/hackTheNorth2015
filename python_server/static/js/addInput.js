$(document).ready(function() {
	$("#searchSubmit").on('click', function (event) {
		event.preventDefault();

		$("#resultText").fadeOut();
		$("#result").fadeOut();
		$(this).text('Loading...');

		var searchName = $('input[name="searchName"]').val();
		var reddit = $('input[name="reddit"]').val();
		var twitter = $('input[name="twitter"]').val();
		$.ajax({
			url: "/search",
			type: "post",
			data: {
				searchName : searchName,
				"reddit" : searchName,
				"twitter" : twitter
			},
			success: function(result) {
				$("#resultText").fadeIn();
				$("#result").html(result.score);
				$("#result").fadeIn();
				$(this).val('Sentimentalize!');
			}
		});
	});
});