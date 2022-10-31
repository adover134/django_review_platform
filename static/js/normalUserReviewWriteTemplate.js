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

function review_submit(e) {
    // preventing from page reload and default actions
    e.preventDefault();
    document.getElementById('review_sentence1').value = document.getElementById('review_sentence').innerText
    // serialize the data for sending the form data.
    var form = new FormData(e.currentTarget);
    const URLSearch = new URLSearchParams(location.search);
    if (URLSearch.has('id')) {
        alert("if문-리뷰수정")
        // var reviewForm = new FormData($('text_review')[0])
        var form = new FormData(e.currentTarget);
        $.ajaxSetup({
            headers: { "X-CSRFToken": "{{csrf_token}}" }
        });
        $.ajax({
                type: 'PUT',
                url: "../normal_user_review_update/",
                async: false,
                processData: false,
                contentType: false,
                data: form,
                success: function (response){
                    alert("리뷰가 수정되었습니다.")
                    window.location.replace('/normal_user_review_read/?id='+response);
                },
                error: function (e){
                    alert("리뷰 수정에 실패하였습니다.")
                }
            })
    }
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