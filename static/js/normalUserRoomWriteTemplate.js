$("#room").submit(room_submit);
function room_submit(e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // serialize the data for sending the form data.
    var form = new FormData(e.currentTarget);
    const URLSearch = new URLSearchParams(location.search);
    var checkbox = $("#room").find("input[type=checkbox]");
    console.log(checkbox);
    $.each(checkbox, function(key, val) {
        form.append($(val).attr('name'), $(this).is(':checked'))
    });
    if (window.location.pathname==='/normal_user_room_change/') {
        // var reviewForm = new FormData($('text_review')[0])
        $.ajax({
            type: 'POST',
            url: "/normal_user_room_update/?roomId="+URLSearch.get('roomId'),
            async: false,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                // on successfull creating object
                window.location.replace('/normal_user_room_read/?roomId='+response);
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
            url: "/normal_user_room_write/",
            async: false,
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                // on successfull creating object
                console.log(response);
                window.location.replace('/normal_user_room_read/?roomId='+response);
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
    roomChangePage();
    if(window.location.pathname==='/normal_user_room_change/'){
        document.getElementById('id_address').readOnly=true;
        document.getElementById('id_postcode').readOnly=true;
        document.getElementById('id_address').removeEventListener("click", map);
    }
}