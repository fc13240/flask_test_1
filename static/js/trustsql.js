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

		var data = {
			'pInfoKey': pInfoKey,
			'nInfoVersion': nInfoVersion,
			'nState': nState,
			'pContent': JSON.stringify(pContent),
			'pNotes': JSON.stringify(pNotes),
			'pCommitTime': pCommitTime,
			'pPrvkey': pPrvkey
		};

		$.ajax({
			url: '/trustsql/issSign',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data) {
			console.log("success");
			console.log(data);
			$('#issSignResult').text(data['sign']);
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	});

	$('#trustsql_issAppend').click(function() {
		console.log('start issAppend');

		var pInfoKey = $('#iss_append_form_pInfoKey').val();
		var nInfoVersion = $('#iss_append_form_nInfoVersion').val();
		var nState = $('#iss_append_form_nState').val();
		// var pContent = $('#iss_append_form_pContent').val();
		// var pNotes = $('#iss_append_form_pNotes').val();
		// var pCommitTime = $('#iss_append_form_pCommitTime').val();

		var pContent = {
			"id": "111111",
			"author": "yuham"
		};

		var pNotes = {
			"note": "stupid man",
			"desc": "hahahahahaha"
		};

		var pCommitTime = '2017-12-20 14:30:00'

		var data = {
			'pInfoKey': pInfoKey,
			'nInfoVersion': nInfoVersion,
			'nState': nState,
			'pContent': JSON.stringify(pContent),
			'pNotes': JSON.stringify(pNotes),
			'pCommitTime': pCommitTime
		};

		$.ajax({
			url: '/trustsql/issAppend',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data) {
			console.log("success");
			console.log(data);
			$('#issSignResult').text(data);
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	});

	$('#trustsql_issQuery').click(function() {
		console.log('start issQuery');

		var data = {
		};

		$.ajax({
			url: '/trustsql/issQuery',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data) {
			console.log("success");
			console.log(data);
			$('#issQueryResult').text(data);
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	})
})