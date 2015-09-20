$(document).ready(function() {
	$("#searchSubmit").on('click', function (event) {
		event.preventDefault();
		$(this).unbind('click').text('Loading...');

		var searchName = $('input[name="searchName"]').val();

		$.ajax({
			url: "/search",
			type: "post",
			data: {
				searchName : searchName
			},
			success: function(result) {
				parsed = $.parseJSON(result);
				$("#result").html(parsed.score);
			}
		});
	});
});