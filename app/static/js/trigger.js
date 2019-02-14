$("button.recommend_trigger").on('click', function() {
    let req_type = $(this).data('trigger');
    $.ajax({
        url: "/user/recommend/",
        type: "POST",
        headers: {
            'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
        },
        data: {
            'type': req_type
        },
        success: function(resp) {
            let movies = resp.data,
                target = resp.type,
                ratings = resp.ratings,
                $target = $(`div.panel-body[data-target=${target}]`);
            $target.empty();
            movies.forEach((movie) => {
                const markup = `
                <div class="col-xs-12 col-md-4">
                    <div class="thumbnail">
                        <img src="${movie.Poster}" alt="Movie Poster">
                        <div class="caption">
                            <h3>"${movie.Title}"</h3>
                            <p>${movie.Plot}</p>
                            <p>
                                <a href="https://www.imdb.com/title/${movie.imdbID}/" class="btn btn-primary" role="button">
                                    <span class="glyphicon glyphicon-link" aria-hidden="true"></span>
                                </a>
                                <a href="/movies/${movie.imdbID}" class="btn btn-default" role="button">
                                    <span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>
                                </a>
                            </p>
                            <p>
                                <input type="range" class="slider" id="${movie.imdbID}" min=0 max=10 step=0.1 value="${ (ratings[movie.imdbID])? ratings[movie.imdbID] : null  }">
                                <label class="label label-primary rating-sliders" data-id="${movie.imdbID}">${ (ratings[movie.imdbID])? ratings[movie.imdbID] : null }</label>
                            </p>
                        </div>
                    </div>
                </div>`;
                    let $data = $.parseHTML(markup)[1];
                $target.append($data);
            });
        }
    });
});
