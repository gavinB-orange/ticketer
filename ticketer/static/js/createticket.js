$(function(){
	$('#btnCreateTicket').click(function(){
        console.log("CreateTicket button clicked");
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
                console.log(response)
                console.log("Switching to /userHome")
				window.location.href = "/userHome"
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
