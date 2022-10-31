window.onload=function(){
    a = Array.from(document.getElementsByClassName('pop_writer'));
    a.forEach(function(o){
        b=(o.offsetHeight/16);
        c=(o.offsetWidth/16/o.innerText.length)
        o.style.fontSize=b;
    });
}