$(function() {
	$('#trustsql_signString').click(function() {
		console.log('start sign');

		var prvkey = $('#signString_form_prvkey').val()
		var pStr = $('#signString_form_pStr').val()

		var data = {
			'prvkey': prvkey,
			'pStr': pStr
		}

		$.ajax({
			url: '/trustsql/signString',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data) {
			console.log('ggg');
			console.log(data);
			console.log('success: ' + data);
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