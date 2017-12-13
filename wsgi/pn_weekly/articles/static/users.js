$(function () {
    //When user starts typing in email
    $('#inputEmail').keyup(function () {

        //check backend if user exists
        $.ajax({
            type: 'POST',
            url: '/reg_check_user/',
            data: {
                'email': $('#inputEmail').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: checkRegAnswer,
            dataType: 'json'
        });
    });

    // When user submits account edit form
    $('#form-edit-account').submit(function (event) {

        //stop page refresh
        event.preventDefault();

        //get fields
        var email = $('#edit-email').val();
        var first_name = $('#edit-first-name').val();
        var last_name = $('#edit-last-name').val();
        var phone = $('#edit-phone').val();

        $.ajax({
            type: 'PUT',
            data: {
                "firstName": first_name,
                "lastName": last_name,
                "phone": phone
            },
            dataType: 'json',
            url: '/edit_account/',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            },
            success: function (jsonResponse) {
                $('#edit-account-info').html("<i class=\"fa fa-check\" style=\"color:green;\" aria-hidden=\"true\"></i> Updated account details</span>");
            },
            error: function (error) {
                $('#edit-account-info').html("<i class=\"fa fa-times\" style=\"color:red;\" aria-hidden=\"true\"></i> Could not edit your details</span>");
            }
        });
    });

    // When user submits edit alerts form
    $('#form-edit-alerts').submit(function (event) {

        //stop page refresh
        event.preventDefault();

        //get checkbox values

        var isBusiness = $('#checkbox-business').is(":checked");
        var isMusic = $('#checkbox-music').is(":checked");
        var isSport = $('#checkbox-sport').is(":checked");
        var isTech = $('#checkbox-technology').is(":checked");

        $.ajax({
            type: 'PUT',
            data: {
                "business": +isBusiness,
                "music": +isMusic,
                "sport": +isSport,
                "tech": +isTech
            },
            dataType: 'json',
            url: '/edit_alerts/',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            },
            success: function (jsonResponse) {
                $('#edit-alerts-info').html("<i class=\"fa fa-check\" style=\"color:green;\" aria-hidden=\"true\"></i> Updated email alert preferences</span>");
            },
            error: function (error) {
                $('#edit-alerts-info').html("<i class=\"fa fa-times\" style=\"color:red;\" aria-hidden=\"true\"></i> Could not edit your email alert preferences</span>");
            }
        });
    });


    //When user clicks clear button
    $('#button-checkbox-clear').click(function (event) {

        //stop page refresh
        event.preventDefault();

        // Clear each checkbox
        $('input[type="checkbox"]').each(function () {
            this.checked = false;
        });
    });

    // Remove alerts save response while user is editing checkboxes
    $('input[type="checkbox"]').change(function () {
        $('#edit-alerts-info').html('');
    });

    // Remove account save response while user is editing
    $('input[type="text"]').keyup(function () {
        $('#edit-account-info').html('');
    });


    //When user submits profile picture
    $("#upload_image").change(function (e) {

        var data = new FormData($('#form-upload-image').get(0));

        // only put file if image has been submitted
        if (data.get('image').name !== '') {

            $.ajax({
                url: '/upload_pic/',
                type: 'PUT',
                data: data,
                cache: false,
                processData: false,
                contentType: false,

                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
                },
                success: function (response) {
                    console.log(response);
                    updateImageUI(response);
                    $('#upload-image-info').html("<i class=\"fa fa-check\" style=\"color:green;\" aria-hidden=\"true\"></i> Successfully updated profile image</span>");

                },
                error: function (response) {
                    $('#upload-image-info').html("<i class=\"fa fa-times\" style=\"color:red;\" aria-hidden=\"true\"></i> Could not upload your picture</span>");
                }
            });

        }


    });

});

// Check email availability json and send html response accordingly
//Disable button to avoid user registration with non unique email
function checkRegAnswer(response) {
    if (response.is_available) {
        $('#info').html("<i class=\"fa fa-check\" style=\"color:green;\" aria-hidden=\"true\"></i> This email is available</span>");
        $('#button-signup-submit').prop('disabled', false);
    } else {
        $('#info').html("<i class=\"fa fa-times\" style=\"color:red;\" aria-hidden=\"true\"></i> This email already exists on our system</span>");
        $('#button-signup-submit').prop('disabled', true);
    }
}

function updateImageUI(userId) {
    // We break the cache and force the browser to check for the image again
    $('#img-user-profile').attr('src', '/media/user_images/' + userId + '.png?' + new Date().getTime());
}