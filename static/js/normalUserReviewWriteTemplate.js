$("#text_review").submit(review_submit);
function review_submit(e) {
    // preventing from page reload and default actions
    e.preventDefault();
    document.getElementById('review_sentence1').value = document.getElementById('review_sentence').innerText
    // serialize the data for sending the form data.
    var form = new FormData(e.currentTarget);
    const URLSearch = new URLSearchParams(location.search);
    if (window.location.pathname==='/normal_user_review_change/') {
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
window.onload = function(){
    document.getElementById("id_address").addEventListener("click", function(){ //주소입력칸을 클릭하면
        //카카오 지도 발생
        new daum.Postcode({
            oncomplete: function(data) { //선택시 입력값 세팅
                document.getElementById("id_address").value = data.address; // 주소 넣기
            }
        }).open();
    });
}