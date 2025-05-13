let currentPages = 1
let previous = 0
let next = 0

const getHistoryReservation = (event) => {
    // Fetch data
    $.ajax({
        url:`/api/users/${$("#id").val()}`,
        type:'GET',
        success:(res)=>{
            if(res){
                // Delete div
                $("#historyContent").remove("#historyContent")

                // Init new div
                $("#root").append(`<div id="historyContent" style="display:inline-flex;flex-wrap:wrap" class="justify-content-between"></div>`)
                let contentDiv = $("#historyContent")

                console.log(res)

                // Loop append data
                $.each(res.reservation_user_set, (index, content) => {
                    const time = content.time ? new Date(content.time) : 'Not Found'
                    const book_time = content.book_date ? new Date(content.book_date) : 'Not Found'

                    contentDiv.append(`
                    <div id="IDC${index}" style="border-radius: 10px;border: none;width:45%!important" class="card p-0 my-3 mx-3 placeholder-glow bg-dark text-white" data-aos="fade-up">
                        <img src="${content.tourism_details.img}" class="card-img-top placeholder" width="245" height="200">
            
                        <div class="card-body">
                            <a style="text-decoration-line: none;" class="card-title placeholder text-white" href="/tourism-place/${content.tourism_details.place_id}">
                                <h5>${content.tourism_details.place_name}, ${content.tourism_details.city}</h5>
                            </a>
                            <div class="d-flex flex-column">
                                <p class="card-text placeholder">Created: ${content.time ? `${time.getDate()}-${(time.getMonth()+1)}-${time.getFullYear()} ${time.getHours()}:${time.getMinutes()}` : time}</p>
                                <p class="card-text placeholder">Status: ${content.status ? content.status:''}</p>
                                <p class="card-text placeholder">Book: ${content.book_date ? `${book_time.getDate()}-${(book_time.getMonth()+1)}-${book_time.getFullYear()}` : book_time}</p>
                            </div>
                            <h6 class="placeholder">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                                    <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
                                </svg>
                                ${content.place_ratings}
                            </h6>
                            <div class="d-flex flex-row justify-content-between">
                                <h6>Rp ${content.tourism_details.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")}</h6>
                                <a class="btn btn-light text-dark" href="/account/reservation-receipt/${content.reservation_id}">Get Receipt</a>
                            </div>
                            
                        </div>
                    </div>
                    `)
                });
            
                $(".placeholder-glow").removeClass("placeholder-glow");
                $(".placeholder").removeClass("placeholder");

                previous = res.previous;
                next = res.next;
            }
        },
        error:(err)=>{
            console.log(err.message);
        }
    });
}

$(document).ready((event)=>{
    getHistoryReservation(event);
});