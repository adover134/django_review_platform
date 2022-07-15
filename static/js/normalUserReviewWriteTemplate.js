function to_image(){
    document.getElementById('text_review').style.display='none';
    document.getElementById('image_review').style.display='inline-block';
    document.getElementById('icons').style.display='inline-block';
}
function to_text(){
    document.getElementById('text_review').style.display='block';
    document.getElementById('image_review').style.display='none';
    document.getElementById('icons').style.display='none';
}

$("#text_review").submit(function review_submit(e) {
    // preventing from page reload and default actions
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    console.log(serializedData);
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: "http://127.0.0.1:8000/test/normal_user_review_write/",
        async: false,
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            $("#text_review").trigger('reset');
            review_num = parseInt(response);
            $("#text_review").action='http://127.0.0.1:8000/test/normal_user_review_read/?id='+response;
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    })
})
$("#image_review").submit(function review_submit(e) {
    // preventing from page reload and default actions
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    console.log(serializedData);
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: "http://127.0.0.1:8000/test/normal_user_review_write/",
        async: false,
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            $("#image_review").trigger('reset');
            review_num = parseInt(response);
            $("#image_review").action='http://127.0.0.1:8000/test/normal_user_review_read/?id='+response;
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    })
})