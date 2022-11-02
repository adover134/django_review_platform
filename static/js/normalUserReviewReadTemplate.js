// 선택된 아이콘 객체를 넣는다.
var selected_icon = null;
// 아이콘 번호를 넣는다.
var selected_num;
// 선택된 아이콘이 있을 경우 해당 아이콘의 미선택 상태의 이미지 위치를 넣는다.
var unselect_image;
var sentence = $('#row4').find('span');
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
        sentence[icons[a][i]].style.color='#A23355';
}
function tak(){
    console.log(reviews);
    for(var i=0;i<sentence.length;i++)
        sentence[i].style.color = 'black';
}
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
window.onload = function()
{
    let a = Array.from(document.getElementById('row3').children);
    a.forEach(function (o) {
        let b = o.offsetHeight / 16;
        let c = o.offsetWidth - o.offsetHeight;
        let d = o.innerText;
        c = (c / d.length) / 16;
        if (b > c)
            o.style.fontSize = c.toString() + 'rem';
        else
            o.style.fontSize = b.toString() + 'rem';
    });
    a=document.getElementById('writer');
    b=(a.offsetHeight/16).toString()+'rem';
    a.style.fontSize=b;
    a=document.getElementById('review_address');
    b=(a.offsetHeight/16).toString()+'rem';
    a.style.fontSize=b;
    a=document.getElementById('review_update');
    b=(a.offsetHeight/16).toString();
    var c=(a.offsetWidth/16/a.innerText.length).toString();
    if (b<c)
        a.style.fontSize=b+'rem';
    else
        a.style.fontSize=c+'rem';
    a=document.getElementById('review_delete');
    b=(a.offsetHeight/16).toString();
    c=(a.offsetWidth/16/a.innerText.length).toString();
    if (b<c)
        a.style.fontSize=b+'rem';
    else
        a.style.fontSize=c+'rem';
    a=document.getElementById('room_read');
    b=(a.offsetHeight/16).toString();
    c=(a.offsetWidth/16/a.innerText.length).toString();
    if (b<c)
        a.style.fontSize=b+'rem';
    else
        a.style.fontSize=c+'rem';
    a=document.getElementById('title');
    b=(a.offsetHeight/16).toString()+'rem';
    a.style.fontSize=b;
    b=(a.offsetHeight/16).toString()+'rem';
    a.style.fontSize=b;
    a=document.getElementById('icons');
    b=(a.offsetHeight);
    c=$('#icons').find('img');
    for(let i=0;i<c.length;i++)
        c[i].style.height=b.toString()+'px';
    a=document.getElementById('rec_button');
    b=(a.offsetHeight/16).toString();
    c=(a.offsetWidth/16/a.innerText.length).toString();
    if (b<c)
        a.style.fontSize=b+'rem';
    else
        a.style.fontSize=c+'rem';
    a=document.getElementById('rep_button');
    b=(a.offsetHeight/16).toString();
    c=(a.offsetWidth/16/a.innerText.length).toString();
    if (b<c)
        a.style.fontSize=b+'rem';
    else
        a.style.fontSize=c+'rem';
    let k = document.getElementsByClassName('review_preview');
    for (let i=0;i<k.length;i++){
        let o = k[i];
        a=o.offsetHeight/16;
        let l=o.offsetWidth-o.offsetHeight;
        let m = o.innerText;
        let n = (l / m.length)/16;
        if (a > n) {
            o.style.fontSize = (Math.ceil(n*100)/100).toString() + 'rem';
        }
        else
            o.style.fontSize=a.toString()+'rem';
    }
    a = Array.from(document.getElementsByClassName('review_title'));
    a.forEach(function(o){
        b=(o.offsetHeight/16).toString()+'rem';
        o.style.fontSize=b;
    });
    a = Array.from(document.getElementsByClassName('review_preview'));
    a.forEach(function(o){
        b=(o.offsetHeight/16).toString()+'rem';
        o.style.fontSize=b;
    });
}

window.onresize = function()
{
    let a = Array.from(document.getElementById('row3').children);
    a.forEach(function (o) {
        let b = o.offsetHeight / 16;
        let c = o.offsetWidth - o.offsetHeight;
        let d = o.innerText;
        c = (c / d.length) / 16;
        if (b > c)
            o.style.fontSize = c.toString() + 'rem';
        else
            o.style.fontSize = b.toString() + 'rem';
    });
    a=document.getElementById('writer');
    b=(a.offsetHeight/16).toString()+'rem';
    a.style.fontSize=b;
    a=document.getElementById('review_address');
    b=(a.offsetHeight/16).toString()+'rem';
    a.style.fontSize=b;
    a=document.getElementById('review_update');
    b=(a.offsetHeight/16).toString();
    let d = (a.offsetWidth/16/a.innerText.length).toString();
    if (b<d)
        a.style.fontSize=b+'rem';
    else
        a.style.fontSize=d+'rem';
    a=document.getElementById('review_delete');
    b=(a.offsetHeight/16).toString();
    d=(a.offsetWidth/16/a.innerText.length).toString();
    if (b<d)
        a.style.fontSize=b+'rem';
    else
        a.style.fontSize=d+'rem';
    a=document.getElementById('room_read');
    b=(a.offsetHeight/16).toString();
    let c=(a.offsetWidth/16/a.innerText.length).toString();
    if (b<c)
        a.style.fontSize=b+'rem';
    else
        a.style.fontSize=c+'rem';
    a=document.getElementById('title');
    b=(a.offsetHeight/16).toString()+'rem';
    a.style.fontSize=b;
    b=(a.offsetHeight/16).toString()+'rem';
    a.style.fontSize=b;
    a=document.getElementById('icons');
    b=(a.offsetHeight);
    c=$('#icons').find('img');
    for(let i=0;i<c.length;i++)
        c[i].style.height=b.toString()+'px';
    a=document.getElementById('rec_button');
    b=(a.offsetHeight/16);
    c=(a.offsetWidth/16/a.innerText.length);
    if (b<c)
        a.style.fontSize=b.toString()+'rem';
    else
        a.style.fontSize=c.toString()+'rem';
    a=document.getElementById('rep_button');
    b=(a.offsetHeight/16);
    c=(a.offsetWidth/16/a.innerText.length);
    if (b<c)
        a.style.fontSize=b.toString()+'rem';
    else
        a.style.fontSize=c.toString()+'rem';
    let k = document.getElementsByClassName('review_preview');
    for (i=0;i<k.length;i++){
        let o = k[i];
        a=o.offsetHeight/16;
        let l=o.offsetWidth-o.offsetHeight;
        let m = o.innerText;
        let n = (l / m.length)/16;
        if (a > n) {
            o.style.fontSize = (Math.ceil(n*100)/100).toString() + 'rem';
        }
        else
            o.style.fontSize=a.toString()+'rem';
    }
    a = Array.from(document.getElementsByClassName('review_title'));
    a.forEach(function(o){
        b=(o.offsetHeight/16).toString()+'rem';
        o.style.fontSize=b;
    });
    a = Array.from(document.getElementsByClassName('review_preview'));
    a.forEach(function(o){
        b=(o.offsetHeight/16).toString()+'rem';
        o.style.fontSize=b;
    });
}
