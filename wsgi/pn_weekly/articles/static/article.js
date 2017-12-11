$(function () {

    var articleId = $('#article-id').text();

    //when user clicks like button
    $("#button-like-article").on('click', function (e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/like_article/',
            data: {
                'articleId': articleId,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {

                setLikeCount(data.likes);

                if (data.status)
                    $("#button-like-article").css("color", "#007BFF");
                else if (data.status = 'unliked')
                    $("#button-like-article").css("color", "#CCCCCC");
            },
            dataType: 'json'
        });
    });

    //when user clicks submit comment button
    $("#button-submit-comment").on('click', function (e) {
        e.preventDefault();

        var commentInput = $('#input-comment-text').val();
        //only allow users to post comment if it contains text
        if (commentInput !== '') {
            $.ajax({
                type: 'POST',
                url: '/post_comment/',
                data: {
                    'articleId': articleId,
                    'comment': commentInput,
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function (comment) {
                    addCommentToPage(comment)
                },
                dataType: 'json'
            });
        }
    });

    //delegate comments container to handle dynamically added delete button on click
    $('#container-comments').on('click', '.delete-button', function (e) {

        e.preventDefault();

        //get div for that specific comment
        var commentDiv = $(this).parent().parent();

        //get id for specific comment
        var commentId = commentDiv.attr('id');

        $.ajax({
            data: {'commentId': commentId.substring(8)},
            type: 'DELETE',
            url: '/delete_comment/',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            },
            success: function (jsonResponse) {
                removeCommentFromPage(commentId.substring(8))

            },
            error: function (error) {
                alert(error.statusText);
            }
        });
    });
});

function addCommentToPage(comment) {
    $('#container-comments').append('<div id="comment_' + comment.id + '" class="media mb-4"><input hidden value="' + comment.user.id + '" id="commenter-id"/><img height="50" width="50" class="d-flex mr-3 rounded-circle" src="../../static/images/user.png" alt=""><div class="media-body col-md-10"><h5 class="mt-0">' + comment.user.first_name + ' ' + comment.user.last_name + '</h5>' + comment.text + '</div><div class="media-body col-md-2"><button id="button-delete-comment" type="button" class="btn btn-danger btn-sm delete-button">Delete</button></div></div>');
}

function removeCommentFromPage(commentId) {
    $('#comment_' + commentId).fadeOut(500, function () {
        $(this).remove();
    });
}

function setLikeCount(likeCount) {
    $('#text-like-count').val(likeCount)
}


