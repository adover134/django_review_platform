function get_address(){
    document.getElementById('search_address').value = document.getElementById('address1').value;
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
window.onload = function(){
    let searched_address = new URLSearchParams(window.location.search);
    console.log(searched_address);
    if (searched_address){
        document.getElementById("address1").value = new URLSearchParams(window.location.search).get('address');
    }
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
    var c = document.createElement("option");
    var d = document.createElement("option");
    c.innerText='최소 연도';
    d.innerText='최대 연도';
    c.selected=true;
    d.selected=true;
    c.disabled=true;
    d.disabled=true;
    c.style.display='none';
    d.style.display='none';
    document.getElementById('writtenStart').appendChild(c);
    document.getElementById('writtenEnd').appendChild(d);
    var i;
    for (i=1960;i<=2022;i++)
    {
        a = document.createElement("option");
        b = document.createElement("option");
        a.value=i;
        b.value=i;
        a.innerText=i;
        b.innerText=i;
        document.getElementById('writtenStart').appendChild(a);
        document.getElementById('writtenEnd').appendChild(b);
    }
}