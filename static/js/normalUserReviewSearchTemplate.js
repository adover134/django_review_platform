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
    var a = document.createElement("option");
    var b = document.createElement("option");
    a.value=i;
    b.value=i;
    a.innerText=i;
    b.innerText=i;
    document.getElementById('builtFrom').appendChild(a);
    document.getElementById('builtTo').appendChild(b);
}

function get_address(){
    document.getElementById('search_address').value = document.getElementById('address1').value;
}