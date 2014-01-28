$(function() {
		$( "#slider" ).slider({
			value:300,
			min: 300,
			max: 700,
			step: 10,
			slide: function( event, ui ) {
				$( "#amount" ).val( "$" + ui.value );
			}
		});
		$( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );
	});
