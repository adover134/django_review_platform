window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        document.getElementsByName('title')[0].value = null;
        document.getElementsByName('title')[1].value = null;
        document.getElementsByName('address')[0].value = null;
        document.getElementsByName('address')[1].value = null;
        document.getElementsByName('review_sentence')[0].value = null;
        document.getElementsByName('images')[0].files = null;
        document.getElementsByName('images')[1].files = null;
        setTimeout(function (){ alert('중복 작성 방지를 위해 기존 작성 내용을 초기화하였습니다.'); },10);
    }
    else {
        console.log('wow');
    }
});
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