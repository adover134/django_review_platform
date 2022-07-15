var selected_icon = null;
var unselect_icon;
var sentence = document.getElementById("reviewContent").children;
var length = sentence.length;

function selectIcon(e){
    if (selected_icon != null) {
        selected_icon.src = unselect_icon;
    }
    selected_icon = e.children[0];
    unselect_icon = e.children[2].value;
    selected_icon.src=e.children[3].value;
    tok(e.children[1].value);
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