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
        document.getElementById('search_address').value = a;
    }
}
function controlFromInput1(fromSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed1(fromInput, toInput);
    fillSlider1(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    if (from > to) {
        fromSlider.value = to;
        fromInput.value = to;
    } else {
        fromSlider.value = from;
    }
}
function controlToInput1(toSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed1(fromInput, toInput);
    fillSlider1(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    setToggleAccessible1(toInput);
    if (from <= to) {
        toSlider.value = to;
        toInput.value = to;
    } else {
        toInput.value = from;
    }
}
function controlFromSlider1(fromSlider, toSlider, fromInput) {
  const [from, to] = getParsed1(fromSlider, toSlider);
  fillSlider1(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  if (from > to) {
    fromSlider.value = to;
    fromInput.value = to;
  } else {
    fromInput.value = from;
  }
}
function controlToSlider1(fromSlider, toSlider, toInput) {
  const [from, to] = getParsed1(fromSlider, toSlider);
  fillSlider1(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  setToggleAccessible1(toSlider);
  if (from <= to) {
    toSlider.value = to;
    toInput.value = to;
  } else {
    toInput.value = from;
    toSlider.value = from;
  }
}
function getParsed1(currentFrom, currentTo) {
  const from = parseInt(currentFrom.value, 10);
  const to = parseInt(currentTo.value, 10);
  return [from, to];
}
function fillSlider1(from, to, sliderColor, rangeColor, controlSlider) {
    const rangeDistance = to.max-to.min;
    const fromPosition = from.value - to.min;
    const toPosition = to.value - to.min;
    controlSlider.style.background = `linear-gradient(
      to right,
      ${sliderColor} 0%,
      ${sliderColor} ${(fromPosition)/(rangeDistance)*100}%,
      ${rangeColor} ${((fromPosition)/(rangeDistance))*100}%,
      ${rangeColor} ${(toPosition)/(rangeDistance)*100}%, 
      ${sliderColor} ${(toPosition)/(rangeDistance)*100}%, 
      ${sliderColor} 100%)`;
}
function setToggleAccessible1(currentTarget) {
  const toSlider = document.querySelector('#toSlider1');
  if (Number(currentTarget.value) <= 0 ) {
    toSlider.style.zIndex = 2;
  }
  else {
    toSlider.style.zIndex = 0;
  }
}
const fromSlider1 = document.querySelector('#fromSlider1');
const toSlider1 = document.querySelector('#toSlider1');
const fromInput1 = document.querySelector('#fromInput1');
const toInput1 = document.querySelector('#toInput1');
fillSlider1(fromSlider1, toSlider1, '#C6C6C6', '#25daa5', toSlider1);
setToggleAccessible1(toSlider1);
fromSlider1.oninput = () => controlFromSlider1(fromSlider1, toSlider1, fromInput1);
toSlider1.oninput = () => controlToSlider1(fromSlider1, toSlider1, toInput1);
fromInput1.oninput = () => controlFromInput1(fromSlider1, fromInput1, toInput1, toSlider1);
toInput1.oninput = () => controlToInput1(toSlider1, fromInput1, toInput1, toSlider1);
function controlFromInput2(fromSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed(fromInput, toInput);
    fillSlider2(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    if (from > to) {
        fromSlider.value = to;
        fromInput.value = to;
    } else {
        fromSlider.value = from;
    }
}
function controlToInput2(toSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed2(fromInput, toInput);
    fillSlider2(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    setToggleAccessible(toInput);
    if (from <= to) {
        toSlider.value = to;
        toInput.value = to;
    } else {
        toInput.value = from;
    }
}
function controlFromSlider2(fromSlider, toSlider, fromInput) {
  const [from, to] = getParsed2(fromSlider, toSlider);
  fillSlider2(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  if (from > to) {
    fromSlider.value = to;
    fromInput.value = to;
  } else {
    fromInput.value = from;
  }
}
function controlToSlider2(fromSlider, toSlider, toInput) {
  const [from, to] = getParsed2(fromSlider, toSlider);
  fillSlider2(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  setToggleAccessible2(toSlider);
  if (from <= to) {
    toSlider.value = to;
    toInput.value = to;
  } else {
    toInput.value = from;
    toSlider.value = from;
  }
}
function getParsed2(currentFrom, currentTo) {
  const from = parseInt(currentFrom.value, 10);
  const to = parseInt(currentTo.value, 10);
  return [from, to];
}
function fillSlider2(from, to, sliderColor, rangeColor, controlSlider) {
    const rangeDistance = to.max-to.min;
    const fromPosition = from.value - to.min;
    const toPosition = to.value - to.min;
    controlSlider.style.background = `linear-gradient(
      to right,
      ${sliderColor} 0%,
      ${sliderColor} ${(fromPosition)/(rangeDistance)*100}%,
      ${rangeColor} ${((fromPosition)/(rangeDistance))*100}%,
      ${rangeColor} ${(toPosition)/(rangeDistance)*100}%, 
      ${sliderColor} ${(toPosition)/(rangeDistance)*100}%, 
      ${sliderColor} 100%)`;
}
function setToggleAccessible2(currentTarget) {
  const toSlider = document.querySelector('#toSlider2');
  if (Number(currentTarget.value) <= 0 ) {
    toSlider.style.zIndex = 2;
  }
  else {
    toSlider.style.zIndex = 0;
  }
}
const fromSlider2 = document.querySelector('#fromSlider2');
const toSlider2 = document.querySelector('#toSlider2');
const fromInput2 = document.querySelector('#fromInput2');
const toInput2 = document.querySelector('#toInput2');
fillSlider2(fromSlider2, toSlider2, '#C6C6C6', '#25daa5', toSlider2);
setToggleAccessible2(toSlider2);
fromSlider2.oninput = () => controlFromSlider2(fromSlider2, toSlider2, fromInput2);
toSlider2.oninput = () => controlToSlider2(fromSlider2, toSlider2, toInput2);
fromInput2.oninput = () => controlFromInput2(fromSlider2, fromInput2, toInput2, toSlider2);
toInput2.oninput = () => controlToInput2(toSlider2, fromInput2, toInput2, toSlider2);