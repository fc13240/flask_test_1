$(function() {
	$('#trustsql_signString').click(function() {
		console.log('start sign')
		var data = {};
		data = $('#trustsql_signString').serialize();

		$.ajax({
			url: '/trustsql/signString',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data) {
			console.log(data);
			$('#signStringResult').text(data['sign']);
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	})
})