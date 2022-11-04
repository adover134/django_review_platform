let current_URL = new URLSearchParams(window.location.search);
current_URL.delete('page');

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
document.getElementById('builtFrom').appendChild(c);
document.getElementById('builtTo').appendChild(d);
var i;
for (i=1960;i<=2022;i++)
{
    a = document.createElement("option");
    b = document.createElement("option");
    a.value=i;
    b.value=i;
    a.innerText=i;
    b.innerText=i;
    a.style.padding='0';
    b.style.padding='0';
    document.getElementById('builtFrom').appendChild(a);
    document.getElementById('builtTo').appendChild(b);
}
window.onload=function() {
    a = new URLSearchParams(window.location.search).get('address');
    if (a){
        document.getElementById('address2').value = a;
    }
}