var selected_icon = null;
var unselect_icon;
var sentence = document.getElementById("reviewContent").children;
var length = sentence.length;

function selectIcon(e){
    if (selected_icon != null) {
        selected_icon.src = unselect_icon;
    }
    if (selected_icon === e.children[0])
    {
        selected_icon = null;
        tok();
    }
    else
    {
        selected_icon = e.children[0];
        unselect_icon = e.children[2].value;
        selected_icon.src=e.children[3].value;
        tok(e.children[1].value);
    }
    console.log(selected_icon);
}

function tok(a){
    for (var i=0;i<(length-1);i=(i+1))
    {
        if (sentence[i].innerText === a){
            sentence[i].style.color='blue';
        }
        else{
            sentence[i].style.color='black';
        }
    }
}
const csrftoken = Cookies.get('csrftoken');
function toggleRecommend(){
    if (reported){
        alert('이미 신고한 글입니다.');
    }
    else if(userloggedin == false){
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

console.log(userloggedin);
