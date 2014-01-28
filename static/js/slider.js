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

$(function build() {
	if ($( "#slider" ).slider( "value" ) < 400) {
		document.getElementById("build").innerHTML='<a href="/add/19-113-335">AMD A6-6400K 3.9GHz Dual-Core Processor</a>';
	}
});
