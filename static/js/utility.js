// $(document).ready(() => {
// 	// Display loading page
// 	$('#body').addClass('body-onloading')
// });

$(window).on('load',() => {
	// Loading Page
	// setTimeout(() => {
	// 	// Remove loading page
	// 	$('#body').removeClass('body-onloading')
	// 	$('#loading').addClass('container-deactivate')
		
	// 	// Display content page
	// 	$('#content').removeClass('container-deactivate')
	// }, 2000)

	$('.placeholder').removeClass('placeholder');
});


$(window).on('scroll', () => {
	if(window.pageYOffset > 450){
		$('.top-section').addClass('top-button-activate')
	} else {
		$('.top-section').removeClass('top-button-activate')
	}
})
