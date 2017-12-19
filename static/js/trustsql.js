$(function() {
	$('#trustsql_signString').click(function() {
		var prvkey = $('#signString_form_prvkey').val();
		var pStr = $('#signString_form_pStr').val();

		var data = {
			'prvkey': prvkey,
			'pStr': pStr
		};

		$.ajax({
			url: '/trustsql/signString',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data) {
			$('#signStringResult').text(data['sign']);
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	});

	$('#trustsql_issSign').click(function() {
		console.log('start issSign');

		var pInfoKey = $('#iss_form_pInfoKey').val();
		var nInfoVersion = $('#iss_form_nInfoVersion').val();
		var nState = $('#iss_form_nState').val();
		var pContent = $('#iss_form_pContent').val();
		var pNotes = $('#iss_form_pNotes').val();
		var pCommitTime = $('#iss_form_pCommitTime').val();
		var pPrvkey = $('#iss_form_pPrvkey').val();

		console.log(pPrvkey);

		var data = {
			'pInfoKey': pInfoKey,
			'nInfoVersion': nInfoVersion,
			'nState': nState,
			'pContent': pContent,
			'pNotes': pNotes,
			'pCommitTime': pCommitTime,
			'pPrvkey': pPrvkey
		};

		console.log(data);

		$.ajax({
			url: '/trustsql/issSign',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data) {
			console.log("success");
			$('#issSignResult').text(data['sign']);
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
		


	})
})