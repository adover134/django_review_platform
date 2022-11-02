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