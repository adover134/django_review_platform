var l1i = document.getElementById('layout1img');
var l2i = document.getElementById('layout2img');
function sort(){
    let selected = document.getElementById('sort_select_box');
    let a = window.location.href;
    let b = a.indexOf('sorted');
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
    a = Array.from(document.getElementsByClassName('review_preview'));
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
    a = Array.from(document.getElementsByClassName('review_preview'));
    a.forEach(function(o){
        b=(o.offsetHeight/16).toString()+'rem';
        o.style.fontSize=b;
    });
}
function get_layout(){
    var layouts = document.getElementsByName('layout');
    for (var layout of layouts)
    {
        if (layout.checked) {
            document.getElementById('id_레이아웃').value = layout.value;
        }
    }
}
function layout_change(event){
    let checked = event.target;
    if (checked.id === 'layout1img')
    {
        l2i.style.border='none';
        l1i.style.border='2px solid blue';
        document.getElementById('layout1').checked=true;
        document.getElementById('layout2').checked=false;
    }
    if (checked.id === 'layout2img')
    {
        l1i.style.border='none';
        l2i.style.border='2px solid blue';
        document.getElementById('layout1').checked=false;
        document.getElementById('layout2').checked=true;
    }
}
// l1i.addEventListener('click', layout_change)
// l2i.addEventListener('click', layout_change)