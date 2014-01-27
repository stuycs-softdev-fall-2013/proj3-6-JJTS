var brands = new Array()

$("#filters :checkbox" ).click(function() {

    $('#filters :checkbox:not(:checked)').each(function(){
	var tmp = new Array()
	var tmpb=brands.pop()
	for (var y = 0; y < brands.length; y++) {
	    if(tmpb == ($(this).val())){
		
	    }
	    else{
		tmp.push(tmpb);
	    }
	}
	console.log(tmpb);
	for (var x = 0; x < tmp.length; x++) {
	    brands.push(tmp.pop())
	}
    });

    $('#filters :checkbox:checked').each(function(){
	for (var i = 0; i < brands.length; i++) {
	    if(brands[i] == ($(this).val())){
		break;
	    }
	}
	if (i == brands.length){
	brands.push($(this).val())
	}
    });
    
    
    $( 'tr' ).show(); 
    console.log(brands)
    $('tr td.brand').each(function(){
	console.log($(this).val())
	for (var i = 0; i < brands.length; i++) {
	    if(brands[i] == ($(this).text())){
		break;
	    }
	}
	if (i == brands.length){
	    $(this).parent().hide()
	}
    });
});


$('#btnFilter').click(function() {
   
    var min = $('#min').val();

    var max = $('#max').val()

    $('tr').show();

    $('tr td.price').each(function() {
        if ($(this).text() <= min && $(this).text() >= max)
        {
            $(this).parent().hide();
        }
    });
    
});
