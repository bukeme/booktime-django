$(function() {
	$('.btn-number').click(function(e) {
		e.preventDefault();
		fieldName = $(this).attr('data-field');
		console.log(fieldName, 'field');
		type = $(this).attr('data-type');
		var input = $('input[name="'+ fieldName + '"]');
		var currentVal = +input.val();
		console.log(input);
		console.log(currentVal, 'val');
		if (type == 'minus') {
			console.log('minus');
			if (currentVal > input.attr('min')) {
				input.val(currentVal -1).change();
			};
			if (parseInt(input.val()) == input.attr('min')) {
				$(this).attr('disabled', true);
			};
		}
		else if (type == 'plus') {
			console.log('plus');
			if (currentVal < input.attr('max')) {
				input.val(currentVal + 1).change();
				console.log(currentVal);
			};
			if (parseInt(input.val()) == input.attr('max')) {
				$(this).attr('disabled', true);
			};
		};

	});
});