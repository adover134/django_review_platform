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
                console.log(response);
                if(Object.keys(response).includes('room_id'))
                {
                    if(confirm('정보가 없는 원룸입니다. 정보를 입력해 주실래요?')){
                        window.location.replace('/normal_user_review_read/?id='+response['review_id']);
                        //window.location.replace('/normal_user_room_change/?id='+response['room_id']);
                    }
                    else
                        window.location.replace('/normal_user_review_read/?id='+response['review_id']);
                }
                else
                    window.location.replace('/normal_user_review_read/?id='+response['review_id']);
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })}
}
window.onload = function(){
    function map(){ //주소입력칸을 클릭하면
        //카카오 지도 발생
        new daum.Postcode({
            oncomplete: function(data) { //선택시 입력값 세팅
                document.getElementById("id_address").value = data.address; // 주소 넣기
                document.getElementById("id_postcode").value = data.zonecode; // 우편번호 넣기
                document.getElementById('id_address').readOnly=true;
                document.getElementById('id_postcode').readOnly=true;
                document.getElementById('id_address').removeEventListener("click", map);
            }
        }).open();
    }
    document.getElementById("id_address").addEventListener("click", map);
    reviewChangePage();
    if(window.location.pathname==='/normal_user_review_change/'){
        document.getElementById('id_address').readOnly=true;
        document.getElementById('id_postcode').readOnly=true;
        document.getElementById('id_address').removeEventListener("click", map);
    }
}