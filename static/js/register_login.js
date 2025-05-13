let register = false
const toggleLoginRegister = () => {
	$('.form-display').eq(0).toggleClass('form-activate')
	$('.form-display').eq(1).toggleClass('form-activate')
	register = !register
	$('#btn_register_login').text(register ? 'Log in' : 'Register')
}