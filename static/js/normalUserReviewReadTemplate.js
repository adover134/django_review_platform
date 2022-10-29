// 선택된 아이콘 객체를 넣는다.
var selected_icon = null;
// 아이콘 번호를 넣는다.
var selected_num;
// 선택된 아이콘이 있을 경우 해당 아이콘의 미선택 상태의 이미지 위치를 넣는다.
var unselect_image;
var sentence = document.getElementById("row4").children;
var length = sentence.length;

function selectIcon(e){
    if (selected_icon != null) {
        selected_icon.src = unselect_image;
    }
    tak()
    if (selected_icon === e.children[0])
        selected_icon = null;
    else
    {
        selected_icon = e.children[0];
        unselect_image = e.children[1].value;
        selected_icon.src=e.children[2].value;
        selected_num = e.children[3].value;
        tok(parseInt(selected_num));
    }
}

function tok(a){
    for(var i=0;i< icons[a].length;i++)
        document.getElementById('row4').children[icons[a][i]].style.color='#A23355';
}
function tak(){
    var reviews = document.getElementById('row4').children;
    for(var i=0;i<reviews.length;i++)
        reviews[i].style.color = 'black';
}
const csrftoken = Cookies.get('csrftoken');
function toggleRecommend(){
    if (reported){
        alert('이미 신고한 글입니다.');
    }
    else if(userloggedin === false){
        alert('로그인이 필요합니다.');
    }
    else {
        $.ajax({
            type: 'POST',
            url: "/toggleRecommmend/",
            async: false,
            headers: {'X-CSRFToken': csrftoken},
            dataType: 'json',
            data: {
                'review': reviewNum,
                'recommended': recommended
            },
            success: function (response) {
                // on successful creating object
                if (recommended){
                    document.getElementById('rec').src=recommendImg;
                    recommended=false;
                    document.getElementById('recommend_num').innerText = parseInt(document.getElementById('recommend_num').innerText)-1;
                }
                else{
                    document.getElementById('rec').src=recommendedImg;
                    recommended=true;
                    document.getElementById('recommend_num').innerText = parseInt(document.getElementById('recommend_num').innerText)+1;
                }
            },
            error: function (response) {
                // alert the error if any error occured
                alert('error');
            }
        })
    }
}
function toggleReport(){
    if (recommended){
        alert('이미 추천한 글입니다.');
    }
    else if(userloggedin == false){
        alert('로그인이 필요합니다.');
    }
    else {
        $.ajax({
            type: 'POST',
            url: "/toggleReport/",
            async: false,
            headers: {'X-CSRFToken': csrftoken},
            dataType: 'json',
            data: {
                'review': reviewNum,
                'reported': reported
            },
            success: function (response) {
                // on successful creating object
                if (reported){
                    document.getElementById('rep').src=reportImg;
                    reported = false;
                    document.getElementById('report_num').innerText = parseInt(document.getElementById('report_num').innerText)-1;
                }
                else{
                    document.getElementById('rep').src=reportedImg;
                    reported = true;
                    document.getElementById('report_num').innerText = parseInt(document.getElementById('report_num').innerText)+1;
                }
            },
            error: function (response) {
                // alert the error if any error occured
                alert('error');
            }
        })
    }
}
