let currentPages = 1
let previous = 0
let next = 0

const getRecommendation = (event) => {
	// Loading Elements
	loadingElement = `
		<div class="card p-0 my-2 card-tourism item placeholder-glow loading">
			<img class="card-img-top placeholder" width="480" height="300">
			<div class="card-text-special">
				<h6 class="card-title fw-bold placeholder"></h6>
				<h6 class="card-text justify-content-align placeholder"></h6>
				<div class="d-flex flex-row justify-content-between fw-bold">
					<a href="#" class="btn btn-primary placeholder"></a>
					<p class="placeholder"></p>
				</div>
			</div>
		</div>
	`
	
	for(let i=0;i<5;i++){$('#container-horizontal-scrolled').append(loadingElement);}
	
	// Get Data
	$.ajax({
		url:`api/sites/recommendation/`,
		type:'GET',
		data:{
			'user':"{{ user }}"
		},
		success:(res)=>{
			if(res){
				// Recommendation
				$.each(res, (index, content) => {
					$('#container-horizontal-scrolled').append(`
						<div id="RecID${index}" class="card p-0 my-2 card-tourism item" data-aos="fade-down">
							<img class="card-img-top" src="${content.img}" width="480" height="300">
							<div class="card-text-special">
								<h6 class="card-title fw-bold placeholder">${content.place_name}, ${content.city}</h6>
								<h6 class="card-text justify-content-align placeholder">${content.description.substring(0,100)}</h6>
								<div class="d-flex flex-row justify-content-between fw-bold">
									<a href="/tourism-place/${content.place_id}" class="btn btn-primary placeholder">Visit</a>
									<p>${content.category_details.category_name} | ${content.price ? 'Rp '+content.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "."):'Gratis'}</p>
								</div>
							</div>
						</div>
					`)
				});

				$(".loading").remove()

				$(".placeholder-glow").removeClass("placeholder-glow");
				$(".placeholder").removeClass("placeholder");
			}
		},
		error:(err)=>{
			$('#reccContainer').remove();
		}
	})
}

const getAllTourism = (event, currentPages) => {
	// Fetch data
	$.ajax({
		url:`/api/sites`,
		type:'GET',
		data:{
			'page':currentPages,
		},
		success:(res) => {
			if(res){
				// Delete div container content
				$('.content-display').remove(".content-display");

				// Memasukkan div kembali
				let divContent = `<div id="container-horizontal-scrolled" class="d-flex flex-wrap content-display justify-content-evenly"></div>`
				$(".content-tourism").append(divContent)

				let containerContent = $(".content-display")

				$.each(res.results, (index, content) => {
					$(containerContent).append(`
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
						</div>`);
				});
			}

			// Update previous and next
			previous = res.previous
			next = res.next	

			// Delete placeholder
			$(".placeholder-glow").removeClass("placeholder-glow");
			$(".placeholder").removeClass("placeholder");
		},
		error:(err) => {
		}
	});
};

const nextPaginationTourism = (event) => {
	if(next){
		currentPages++;
		getAllTourism(event, currentPages);
	}
}

const previousPaginationTourism = (event) => {
	if(previous){
		currentPages--;
		getAllTourism(event, currentPages);
	}
}

$(document).ready((e) => {
	getAllTourism(e, currentPages);
	getRecommendation(e);
});