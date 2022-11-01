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
const csrftoken = Cookies.get('csrftoken');
function review_submit(e) {
    // preventing from page reload and default actions
    e.preventDefault();
    document.getElementById('review_sentence1').value = document.getElementById('review_sentence').innerText
    // serialize the data for sending the form data.
    var form = new FormData(e.currentTarget);
    const URLSearch = new URLSearchParams(location.search);
    if (window.location.pathname==='/normal_user_review_change/') {
        alert("if문-리뷰수정")
        // var reviewForm = new FormData($('text_review')[0])
        $.ajax({
            type: 'POST',
            url: "/normal_user_review_update/?id="+URLSearch.get('id'),
            async: false,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                // on successfull creating object
                window.location.replace('/normal_user_review_read/?id='+response);
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })}
    else{
        alert("else문-리뷰등록")
    // make POST ajax call
        $.ajax({
            type: 'POST',
            url: "/normal_user_review_write/",
            async: false,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                // on successfull creating object
                window.location.replace('/normal_user_review_read/?id='+response);
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })}
}