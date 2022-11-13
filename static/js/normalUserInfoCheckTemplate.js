function sort(){
    let selected = document.getElementById('sort_select_box');
    let a = window.location.href;
    let b = a.indexOf('sorted');
    if (a.slice(0, b)[b-1] === '/')
        window.location.href = a.slice(0, b)+'?sorted='+document.getElementById('sort_select_box').value;
    window.location.href = a.slice(0, b)+'sorted='+document.getElementById('sort_select_box').value;
}
window.onload=function() {
    let a = new URLSearchParams(window.location.search).get('sorted');
    var b = document.createElement("option");
    switch (a) {
        case '2':
            b.innerText = '추천 순';
            break;
        case '3':
            b.innerText = '정확도 순';
            break;
        case '1':
        default:
            b.innerText = '최신 순';
            break;
    }
    b.selected = true;
    b.style.display = 'none';
    document.getElementById('sort_select_box').appendChild(b);
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
}
window.onresize = function(){
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
}