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
    a=document.getElementById('score_filters');
    let sf1 = a.offsetHeight / 16;
    let sf2 = a.offsetWidth - a.offsetHeight;
    let sf3 = a.innerText;
    sf2 = (sf2 / sf3.length) / 16;
    if (sf1 > sf2)
        a.style.fontSize = sf2.toString() + 'rem';
    else
        a.style.fontSize = sf1.toString() + 'rem';
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
        let b=(o.offsetHeight/16).toString()+'rem';
        o.style.fontSize=b;
    });
    a = Array.from(document.getElementsByClassName('review_preview'));
    a.forEach(function(o){
        let b=(o.offsetHeight/16).toString()+'rem';
        o.style.fontSize=b;
    });
    a=document.getElementById('score_filters');
    let sf1 = a.offsetHeight / 16;
    let sf2 = a.offsetWidth - a.offsetHeight;
    let sf3 = a.innerText;
    sf2 = (sf2 / sf3.length) / 16;
    if (sf1 > sf2)
        a.style.fontSize = sf2.toString() + 'rem';
    else
        a.style.fontSize = sf1.toString() + 'rem';
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
    // document.getElementById('writtenStart').appendChild(c);
    // document.getElementById('writtenEnd').appendChild(d);
    var i;
    for (i=1960;i<=2022;i++)
    {
        a = document.createElement("option");
        b = document.createElement("option");
        a.value=i;
        b.value=i;
        a.innerText=i;
        b.innerText=i;
        // document.getElementById('writtenStart').appendChild(a);
        // document.getElementById('writtenEnd').appendChild(b);
    }
}

const humidityFromSlider = document.querySelector('#humidityFromSlider');
const humidityToSlider = document.querySelector('#humidityToSlider');
const humidityFromInput = document.querySelector('#humidityFromInput');
const humidityToInput = document.querySelector('#humidityToInput');
const soundproofFromSlider = document.querySelector('#soundproofFromSlider');
const soundproofToSlider = document.querySelector('#soundproofToSlider');
const soundproofFromInput = document.querySelector('#soundproofFromInput');
const soundproofToInput = document.querySelector('#soundproofToInput');
const lightingFromSlider = document.querySelector('#lightingFromSlider');
const lightingToSlider = document.querySelector('#lightingToSlider');
const lightingFromInput = document.querySelector('#lightingFromInput');
const lightingToInput = document.querySelector('#lightingToInput');
const cleanlinessFromSlider = document.querySelector('#cleanlinessFromSlider');
const cleanlinessToSlider = document.querySelector('#cleanlinessToSlider');
const cleanlinessFromInput = document.querySelector('#cleanlinessFromInput');
const cleanlinessToInput = document.querySelector('#cleanlinessToInput');

function controlFromInput(fromSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed(fromInput, toInput);
    fillSlider(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    if (from > to) {
        fromSlider.value = to;
        fromInput.value = to;
    } else {
        fromSlider.value = from;
    }
}
function controlFromSlider(fromSlider, toSlider, fromInput) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  if (from > to) {
    fromSlider.value = to;
    fromInput.value = to;
  } else {
    fromInput.value = from;
  }
}

function humiditycontrolToInput(toSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed(fromInput, toInput);
    fillSlider(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    setTogglehumidityAccessible(toInput);
    if (from <= to) {
        toSlider.value = to;
        toInput.value = to;
    } else {
        toInput.value = from;
    }
}
function humiditycontrolToSlider(fromSlider, toSlider, toInput) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  setTogglehumidityAccessible(toSlider);
  if (from <= to) {
    toSlider.value = to;
    toInput.value = to;
  } else {
    toInput.value = from;
    toSlider.value = from;
  }
}
function setTogglehumidityAccessible(currentTarget) {
  const toSlider = document.querySelector('#humidity');
  if (Number(currentTarget.value) <= 0 ) {
    toSlider.style.zIndex = 2;
  }
  else {
    toSlider.style.zIndex = 0;
  }
}

function soundproofcontrolToInput(toSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed(fromInput, toInput);
    fillSlider(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    setTogglesoundproofAccessible(toInput);
    if (from <= to) {
        toSlider.value = to;
        toInput.value = to;
    } else {
        toInput.value = from;
    }
}
function soundproofcontrolToSlider(fromSlider, toSlider, toInput) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  setTogglesoundproofAccessible(toSlider);
  if (from <= to) {
    toSlider.value = to;
    toInput.value = to;
  } else {
    toInput.value = from;
    toSlider.value = from;
  }
}
function setTogglesoundproofAccessible(currentTarget) {
  const toSlider = document.querySelector('#soundproof');
  if (Number(currentTarget.value) <= 0 ) {
    toSlider.style.zIndex = 2;
  }
  else {
    toSlider.style.zIndex = 0;
  }
}

function lightingcontrolToInput(toSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed(fromInput, toInput);
    fillSlider(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    setTogglelightingAccessible(toInput);
    if (from <= to) {
        toSlider.value = to;
        toInput.value = to;
    } else {
        toInput.value = from;
    }
}
function lightingcontrolToSlider(fromSlider, toSlider, toInput) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  setTogglelightingAccessible(toSlider);
  if (from <= to) {
    toSlider.value = to;
    toInput.value = to;
  } else {
    toInput.value = from;
    toSlider.value = from;
  }
}
function setTogglelightingAccessible(currentTarget) {
  const toSlider = document.querySelector('#lighting');
  if (Number(currentTarget.value) <= 0 ) {
    toSlider.style.zIndex = 2;
  }
  else {
    toSlider.style.zIndex = 0;
  }
}

function cleanlinesscontrolToInput(toSlider, fromInput, toInput, controlSlider) {
    const [from, to] = getParsed(fromInput, toInput);
    fillSlider(fromInput, toInput, '#C6C6C6', '#25daa5', controlSlider);
    setTogglecleanlinessAccessible(toInput);
    if (from <= to) {
        toSlider.value = to;
        toInput.value = to;
    } else {
        toInput.value = from;
    }
}
function cleanlinesscontrolToSlider(fromSlider, toSlider, toInput) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
  setTogglecleanlinessAccessible(toSlider);
  if (from <= to) {
    toSlider.value = to;
    toInput.value = to;
  } else {
    toInput.value = from;
    toSlider.value = from;
  }
}
function setTogglecleanlinessAccessible(currentTarget) {
  const toSlider = document.querySelector('#cleanliness');
  if (Number(currentTarget.value) <= 0 ) {
    toSlider.style.zIndex = 2;
  }
  else {
    toSlider.style.zIndex = 0;
  }
}

function getParsed(currentFrom, currentTo) {
  const from = parseInt(currentFrom.value, 10);
  const to = parseInt(currentTo.value, 10);
  return [from, to];
}
function fillSlider(from, to, sliderColor, rangeColor, controlSlider) {
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

fillSlider(humidityFromSlider, humidityToSlider, '#C6C6C6', '#25daa5', humidityToSlider);
fillSlider(soundproofFromSlider, soundproofToSlider, '#C6C6C6', '#25daa5', soundproofToSlider);
fillSlider(lightingFromSlider, lightingToSlider, '#C6C6C6', '#25daa5', lightingToSlider);
fillSlider(cleanlinessFromSlider, humidityToSlider, '#C6C6C6', '#25daa5', cleanlinessToSlider);

setTogglehumidityAccessible(humidityToSlider);
setTogglesoundproofAccessible(soundproofToSlider);
setTogglelightingAccessible(lightingToSlider);
setTogglecleanlinessAccessible(cleanlinessToSlider);

humidityFromSlider.oninput = () => controlFromSlider(humidityFromSlider, humidityToSlider, humidityFromInput);
humidityToSlider.oninput = () => humiditycontrolToSlider(humidityFromSlider, humidityToSlider, humidityToInput);
humidityFromInput.oninput = () => controlFromInput(humidityFromSlider, humidityFromInput, humidityToInput, humidityToSlider);
humidityToInput.oninput = () => humiditycontrolToInput(humidityToSlider, humidityFromInput, humidityToInput, humidityToSlider);

soundproofFromSlider.oninput = () => controlFromSlider(soundproofFromSlider, soundproofToSlider, soundproofFromInput);
soundproofToSlider.oninput = () => soundproofcontrolToSlider(soundproofFromSlider, soundproofToSlider, soundproofToInput);
soundproofFromInput.oninput = () => controlFromInput(soundproofFromSlider, soundproofFromInput, soundproofToInput, soundproofToSlider);
soundproofToInput.oninput = () => soundproofcontrolToInput(soundproofToSlider, soundproofFromInput, soundproofToInput, soundproofToSlider);

lightingFromSlider.oninput = () => controlFromSlider(lightingFromSlider, lightingToSlider, lightingFromInput);
lightingToSlider.oninput = () => lightingcontrolToSlider(lightingFromSlider, lightingToSlider, lightingToInput);
lightingFromInput.oninput = () => controlFromInput(lightingFromSlider, lightingFromInput, lightingToInput, lightingToSlider);
lightingToInput.oninput = () => lightingcontrolToInput(lightingToSlider, lightingFromInput, lightingToInput, lightingToSlider);

cleanlinessFromSlider.oninput = () => controlFromSlider(cleanlinessFromSlider, cleanlinessToSlider, cleanlinessFromInput);
cleanlinessToSlider.oninput = () => cleanlinesscontrolToSlider(cleanlinessFromSlider, cleanlinessToSlider, cleanlinessToInput);
cleanlinessFromInput.oninput = () => controlFromInput(cleanlinessFromSlider, cleanlinessFromInput, cleanlinessToInput, cleanlinessToSlider);
cleanlinessToInput.oninput = () => cleanlinesscontrolToInput(cleanlinessToSlider, cleanlinessFromInput, cleanlinessToInput, cleanlinessToSlider);