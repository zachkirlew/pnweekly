$(function () {




    //when category is clicked
    $('.button-filter').on('click', function (e) {
        e.preventDefault();

        var stringFilter = $(this).attr("name");
        getFilteredArticles(stringFilter)
    });

    function getFilteredArticles(stringFilter) {
        //filter articles
        $.ajax({
            type: 'GET',
            url: '/filter_articles/' + stringFilter,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                clearArticles();
                addArticlesToPage(data);
            },
            error: function (error) {
                console.log(error.message);
            }
        });
    }

    function addArticlesToPage(data) {

        //for each article append to html
        $.each(data, function (index, article) {
            $('#container-news').append('<div class="card mb-4"><img src="' + article.image_url + '" class="card-img-top" src="http://placehold.it/750x300" alt="Card image cap"><div class="card-body"><h2 class="card-title">' + article.title + '</h2><p class="card-text">' + article.description + '</p><a href="/article_detail/' + article.id + '" class="btn btn-primary">Read More &rarr;</a></div><div class="card-footer text-muted">' + article.published_at + ' by ' + article.author + '</div></div>');
        });
    }

    function clearArticles(){
        $('#container-news').html('');
    }


});




