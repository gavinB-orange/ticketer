$(function(){
	$('#btnSignUp').click(function(){
        console.log("Signup button clicked");
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
                console.log(response)
                console.log("Switching to showSignIn")
				window.location.href = "/showSignIn"
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
