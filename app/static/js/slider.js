$(document).ready(function() {
    $("div.movie-holder").on('input', 'div.thumbnail input.slider',  debounce(function() {
        let val = $(this).val();
        $(this).closest('p').find('label.rating-sliders').text(val);
        $.ajax({
            url: "/movies/updateRating/",
            type: "POST",
            headers: {
                'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
            },
            data: {
                'rating': parseFloat(val),
                'imdbID': $(this).attr('id')
            },
            success: function(resp) {
                if(!resp.status) {
                    alert(resp.error + " Please login!");
                    window.location.replace('/user/signin/');
                }
            }
        });
    }, 100));
});
