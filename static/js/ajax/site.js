// Toast Template
const toastSuccessTemplate = `
<div id="liveToast" class="toast align-items-center bg-success" role="alert" aria-live="assertive" aria-atomic="true">
	<div class="d-flex text-white" data-aos="fade-up">
		<div class="toast-body">
			Action has successfuly been processed, <a href="#">view details</a>.
		</div>
		<button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
	</div>
</div>
`

const toastErrorTemplate = `
<div id="liveToast" class="toast align-items-center bg-danger" role="alert" aria-live="assertive" aria-atomic="true">
	<div class="d-flex text-white" data-aos="fade-up">
		<div class="toast-body">
			Action has not been processed, <a href="#">view details</a>.
		</div>
		<button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
	</div>
</div>
`

const dateFormat = new Intl.DateTimeFormat('default', { month: 'short' });

const ratingsCalculator = (mean, max, total_counts, count, threshold=0.5) => {
	const WR = ((mean / max)*threshold*100) + ((count/total_counts)*(1-threshold)*100)
	return WR/10
}


$(document).ready((e) => {
	idFromURL = window.location.href.split('/').slice(-1)[0]

	// Get Site Information
	$.ajax({
		url:`/api/sites/${idFromURL}`,
		type:'GET',
		success:(res) => {
			console.log(res)
			if(res){
				$("title").html(`${res.data.place_name}, ${res.data.city}`)

				$("#Img").attr('src',res.data.img)
				$("#Title").text(`${res.data.place_name}, ${res.data.city}`)
				$("#Desc").text(res.data.description)
				$("#Price").text(`Rp.  ${res.data.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")}`)

				let sum = 0
				let count = 0
				$.each(res.data.reservation_place_set, (index, content)=>{
					time = content.time ? `${dateFormat.format(new Date(content.time).getMonth()+1)}, ${new Date(content.time).getFullYear()}` : '';
					sum += content.place_ratings
					count += 1
					$("#ratingComments #container-horizontal-scrolled").append(`
						<div id="feedback${index}" class="item">
							<h4>${content.user_details.email ? content.user_details.email.split('@')[0]:'Anonymous'}</h4>
							<h5>
								<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="yellow" class="bi bi-star-fill" viewBox="0 0 16 16">
									<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
								</svg>
								${content.place_ratings}
							</h5>
							<p>${time}</p>
							<p>${content.comments ? content.comments:''}</p>
						</div>
					`);
				});

				let mean = sum / count

				sum = ratingsCalculator(mean, 5, res.count, count, threshold=0.5)
				sum = sum ? Math.round(sum * 10)/10 : 0.0

				$("#ratingScore").text(sum)
				$("#Ratings").append(sum)

				for(let i=1;i<=5;i++){
					if(i<=sum){
						$('#ratingStar').append(`
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="yellow" class="bi bi-star-fill" viewBox="0 0 16 16">
								<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
							</svg>
						`)
					} else if(sum-Math.floor(sum) >= 0.5){
						sum = Math.ceil(sum)
						$('#ratingStar').append(`
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="yellow" class="bi bi-star-half" viewBox="0 0 16 16">
								<path d="M5.354 5.119 7.538.792A.516.516 0 0 1 8 .5c.183 0 .366.097.465.292l2.184 4.327 4.898.696A.537.537 0 0 1 16 6.32a.548.548 0 0 1-.17.445l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256a.52.52 0 0 1-.146.05c-.342.06-.668-.254-.6-.642l.83-4.73L.173 6.765a.55.55 0 0 1-.172-.403.58.58 0 0 1 .085-.302.513.513 0 0 1 .37-.245l4.898-.696zM8 12.027a.5.5 0 0 1 .232.056l3.686 1.894-.694-3.957a.565.565 0 0 1 .162-.505l2.907-2.77-4.052-.576a.525.525 0 0 1-.393-.288L8.001 2.223 8 2.226v9.8z"/>
							</svg>
						`)
					} else {
						$('#ratingStar').append(`
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="yellow" class="bi bi-star" viewBox="0 0 16 16">
								<path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
							</svg>
						`)
					} 
				}

				// Init confirmation place values
				$("#placeName").text(res.data.place_name)
				$("#placePrice").text(res.data.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "."))
				$("#placeLocation").text(`Lat:${res.data.lat} Long:${res.data.long}`)	
				$("#placeId").val(res.data.place_id)


				// Init min book date
				dateNow = new Date()
				dd = String(dateNow.getDate()).padStart(2, 0)
				mm = String(dateNow.getMonth()+1).padStart(2, 0)
				yyyy = dateNow.getFullYear()

				$("#bookDate").attr('min', `${yyyy}-${mm}-${dd}`)
			}
		},
		error:(err) => {
			$("#liveToast").remove()
			$("#toastNotifSuccess").append(toastErrorTemplate)
			
			const toast = new bootstrap.Toast($("#liveToast"))
			toast.show()
		}
	});

	// Get Similar Site
	$.ajax({
		url:`/api/sites/similar/${idFromURL}`,
		type:'GET',
		success:(res)=>{
			if(res){
				$.each(res, (index, content)=>{
					$(".similar-reccomendation").append(`
						<div id="ID_${content.place_id}" class="card p-0 my-2 card-tourism item placeholder-glow" data-aos="fade-up">
							<img class="card-img-top placeholder" src="${content.img}" width="480" height="300">
							<div class="card-text-special">
								<h6 class="card-title fw-bold placeholder">${content.place_name}, ${content.city}</h6>
								<h6 class="card-text justify-content-align placeholder">${content.description.substring(0,100)}...</h6>
								<div class="d-flex flex-row justify-content-between fw-bold">
									<a href="/tourism-place/${content.place_id}" class="btn btn-primary placeholder">Visit</a>
									<p>${content.category_details.category_name} | ${content.price ? 'Rp '+content.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "."):'Gratis'}</p>
								</div>
							</div>
						</div>
					`)
				})

				// Remove placeholder
				$(".placeholder").removeClass("placeholder")
				$(".placeholder-glow").removeClass("placeholder-glow")
			}
		},
		error:(err)=>{
			$("#liveToast").remove()
			$("#toastNotifSuccess").append(toastErrorTemplate)
			
			const toast = new bootstrap.Toast($("#liveToast"))
			toast.show()
		}
	});
});

$(window).on('load', (e)=>{
	$(".placeholder-glow").removeClass("placeholder-glow");
	$(".placeholder").removeClass("placeholder");

	// $("#bookDate").attr("min", new Date().toISOString().split("T")[0])
});

$("#formReservation").on('submit', (e)=> {
	e.preventDefault();
	
	$.ajaxSetup({
		headers: { 
			"X-CSRFToken": $('#formReservation').serialize().split("&")[0].split("=")[1]
		}
	});

	$.ajax({
		url:'/api/reservation/',
		type:'POST',
		data:$('#formReservation').serialize(),
		success:(res)=>{

			// Close Modal
			$(".btn-close").click();
			
			$("#liveToast").remove()
			$("#toastNotifSuccess").append(toastSuccessTemplate)
			
			const toast = new bootstrap.Toast($("#liveToast"))
			toast.show()
		},
		error:(err)=>{
			$("#liveToast").remove()
			$("#toastNotifSuccess").append(toastErrorTemplate)
			
			const toast = new bootstrap.Toast($("#liveToast"))
			toast.show()
		}
	});
});

$("#formFeedback").on('submit', (e)=>{
	e.preventDefault();

	// Close Modal
	$(".btn-close").click();

	$.ajaxSetup({
		headers: {
			'X-CSRFToken': $('#formFeedback').serialize().split("&")[0].split("=")[1],
			'X-HTTP-Method-Override': 'PATCH'
		}
	});

	$.ajax({
		url:`/api/sites/rating/${window.location.href.split("/")[4]}`,
		type:"PATCH",
		data:$("#formFeedback").serialize()+"&user={{ user }}",
		success:(res)=>{
			// Close Modal
			$(".btn-close").click();
			
			// Notification
			$("#liveToast").remove();
			$("#toastNotifSuccess").append(toastSuccessTemplate)
			
			const toast = new bootstrap.Toast($("#liveToast"))
			toast.show()
		},
		error:(err)=>{
			$("#liveToast").remove();
			$("#toastNotifSuccess").append(toastErrorTemplate)
			
			const toast = new bootstrap.Toast($("#liveToast"))
			toast.show()
		}
	});
});