var brands = new Array()

$("#filters :checkbox" ).click(function() {
    var chker = new Array()
//Removes any item from the array that is unchecked
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

	for (var i = 0; i < tmp.length; i++) {
	    chker[i] = tmp[i]
	}
	
	for (var x = 0; x < tmp.length; x++) {
	    brands.push(tmp.pop())
	}
    });
    console.log(chker)
//Adds any checked item into Array
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
    
    console.log(chker)
    
    if(chker.length != 0){
	brands = chker
    }
    
    //Filters out the table
    $( 'tr' ).show(); 
    console.log(brands)
    $('tr td.brand').each(function(){
	for (var i = 0; i < brands.length; i++) {
	    if(brands[i] == ($(this).text().split(" ",1))){
		break;
	    }
	}
	if (i == brands.length){
	    $(this).parent().hide()
	}
    });
    
    if (brands.length == 0){
	$( 'tr' ).show(); 
    }
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
