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

$("#text_review").submit(review_submit)

$("#image_review").submit(review_submit)

function review_submit(e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: "http://127.0.0.1:8000/test/normal_user_review_write/",
        async: false,
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            $("#"+this.id).trigger('reset');
            window.location.replace('http://127.0.0.1:8000/test/normal_user_review_read/?id='+response);
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    })
}