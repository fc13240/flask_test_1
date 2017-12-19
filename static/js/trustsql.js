$(function() {
	$('#trustsql_signString').click(function() {
		var prvkey = $('#signString_form_prvkey').val();
		var pStr = $('#signString_form_pStr').val();

		console.log('get vals');
		// console.log(prvkey);
		// console.log(pStr);

		var data = {
			'prvkey': prvkey,
			'pStr': pStr
		};

		console.log(data);

		$.ajax({
			url: '/trustsql/signString',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data) {
			console.log('ggg');
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