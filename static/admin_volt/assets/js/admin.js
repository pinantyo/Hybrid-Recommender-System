$('#optionModelForm').on("submit", (e) => {
    e.preventDefault();

    $.ajaxSetup({
		headers: { 
			"X-CSRFToken": $('#optionModelForm').serialize().split("&")[0].split("=")[1]
		}
	});
    
    $.ajax({
        url:'api/utilize-model',
        type:'POST',
        data:{
            'user':"{{ user }}",
            'model_name':$('#modelOption option:selected').val(),
            'mode':$('#modelMode option:selected').val()
        },
        success: (res) => {
            if(res){
                console.log(res);
            }
        },
        error: (err) => {
            console.log(err);
        }
    });
});