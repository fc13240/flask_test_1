function signString() {
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
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
	
}