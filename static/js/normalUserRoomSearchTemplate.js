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

const inputLeft = document.getElementById("input-left");
const inputRight = document.getElementById("input-right");

const thumbLeft = document.querySelector(".thumb.left");
const thumbRight = document.querySelector(".thumb.right");

const range = document.querySelector(".range");

const setLeftValue = e => {
  const _this = e.target;
  const { value, min, max } = _this;

  if (+inputRight.value - +value < 10) {
    _this.value = +inputRight.value - 10;
  }

  const percent = ((+_this.value - +min) / (+max - +min)) * 100;

  thumbLeft.style.left = `${percent}%`;
  range.style.left = `${percent}%`;
};

const setRightValue = e => {
  const _this = e.target;
  const { value, min, max } = _this;

  if (+value - +inputLeft.value < 10) {
    _this.value = +inputLeft.value + 10;
  }

  const percent = ((+_this.value - +min) / (+max - +min)) * 100;

  thumbRight.style.right = `${100 - percent}%`;
  range.style.right = `${100 - percent}%`;
};

if (inputLeft && inputRight) {
  inputLeft.addEventListener("input", setLeftValue);
  inputRight.addEventListener("input", setRightValue);
}



const inputLeft2 = document.getElementById("input-left2");
const inputRight2 = document.getElementById("input-right2");

const thumbLeft2 = document.querySelector(".thumb.left2");
const thumbRight2 = document.querySelector(".thumb.right2");

const range2 = document.querySelector(".range2");

const setLeftValue2 = e => {
  const _this = e.target;
  const { value, min, max } = _this;

  if (+inputRight2.value - +value < 1) {
    _this.value = +inputRight2.value - 1;
  }

  const percent = ((+_this.value - +min) / (+max - +min)) * 100;

  thumbLeft2.style.left = `${percent}%`;
  range2.style.left = `${percent}%`;
};

const setRightValue2 = e => {
  const _this = e.target;
  const { value, min, max } = _this;

  if (+value - +inputLeft2.value < 1) {
    _this.value = +inputLeft2.value + 1;
  }

  const percent = ((+_this.value - +min) / (+max - +min)) * 100;

  thumbRight2.style.right = `${100 - percent}%`;
  range2.style.right = `${100 - percent}%`;
};

if (inputLeft2 && inputRight2) {
  inputLeft2.addEventListener("input", setLeftValue2);
  inputRight2.addEventListener("input", setRightValue2);
}

