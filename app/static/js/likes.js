$(document).ready(function() {
    let updateList = (likedOrNot) => {
        let name_type = (likedOrNot)? "liked" : "disliked";
        let selected = $(`input[name='${name_type}']:checked`).map((_, el) => $(el).val()).get();

        $.ajax({
            url: '/user/',
            type: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
            },
            data: {
                'updatedList': selected,
                'likedOrNot': likedOrNot
            }
        });
    };
    $("input[name='liked']").change(function(e) {
        updateList(true);
    });
    $("input[name='disliked']").change(function(e) {
        updateList(false);
    });
});