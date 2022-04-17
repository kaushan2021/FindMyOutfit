finalGender = null;
finalAge = null;
finalDressCode = null;
finalSkinTone = null;
finalSeason = null;

const wrapper4 = document.querySelector(".wrapper4"),
selectBtn4 = wrapper4.querySelector(".select-btn4"),
searchInp4 = wrapper4.querySelector("input4"),
options4 = wrapper4.querySelector(".options");

let Gender = ["Male", "Female"];

function addGender(selectedGender) {
    options4.innerHTML = "";
    Gender.forEach(DressCode => {
        let isSelected4 = DressCode == selectedGender ? "selected" : "";
        let li4 = `<li onclick="updateGender(this)" class="${isSelected4}">${DressCode}</li>`;
        options4.insertAdjacentHTML("beforeend", li4);
    });
}
addGender();

function updateGender(selectedLi4) {
    
    addGender(selectedLi4.innerText);
    wrapper4.classList.remove("active4");
    selectBtn4.firstElementChild.innerText = selectedLi4.innerText;
    finalGender = selectedLi4.innerText;
}

selectBtn4.addEventListener("click", () => wrapper4.classList.toggle("active4"));



const wrapper5 = document.querySelector(".wrapper5"),
selectBtn5 = wrapper5.querySelector(".select-btn5"),
searchInp5 = wrapper5.querySelector("input5"),
options5 = wrapper5.querySelector(".options");

let Age = ["12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100",];

function addAge(selectedAge) {
    options5.innerHTML = "";
    Age.forEach(Age => {
        let isSelected5 = Age == selectedAge ? "selected" : "";
        let li5 = `<li onclick="updateAge(this)" class="${isSelected5}">${Age}</li>`;
        options5.insertAdjacentHTML("beforeend", li5);
    });
}
addAge();

function updateAge(selectedLi5) {
    
    addAge(selectedLi5.innerText);
    wrapper5.classList.remove("active5");
    selectBtn5.firstElementChild.innerText = selectedLi5.innerText;
    finalAge = selectedLi5.innerText;
}

selectBtn5.addEventListener("click", () => wrapper5.classList.toggle("active5"));



const wrapper1 = document.querySelector(".wrapper1"),
selectBtn1 = wrapper1.querySelector(".select-btn1"),
searchInp1 = wrapper1.querySelector("input1"),
options1 = wrapper1.querySelector(".options");

let DressCode = ["Casual", "Sports", "Ethnic", "Formal"];

function addDressCode(selectedDressCode) {
    options1.innerHTML = "";
    DressCode.forEach(DressCode => {
        let isSelected1 = DressCode == selectedDressCode ? "selected" : "";
        let li1 = `<li onclick="updateDressCode(this)" class="${isSelected1}">${DressCode}</li>`;
        options1.insertAdjacentHTML("beforeend", li1);
    });
}
addDressCode();

function updateDressCode(selectedLi1) {
    
    addDressCode(selectedLi1.innerText);
    wrapper1.classList.remove("active1");
    selectBtn1.firstElementChild.innerText = selectedLi1.innerText;
    finalDressCode = selectedLi1.innerText;
}

selectBtn1.addEventListener("click", () => wrapper1.classList.toggle("active1"));



const wrapper2 = document.querySelector(".wrapper2"),
selectBtn2 = wrapper2.querySelector(".select-btn2"),
searchInp2 = wrapper2.querySelector("input2"),
options2 = wrapper2.querySelector(".options");

let SkinTone = ["Porcelain", "Ivory", "Warm Ivory", "Sand", "Beige", "Warm Beige", "Natural", "Honey", "Golden", "Almond", "Chestnut", "Espresso"];

function addSkinTone(selectedSkinTone) {
    options2.innerHTML = "";
    SkinTone.forEach(SkinTone => {
        let isSelected2 = SkinTone == selectedSkinTone ? "selected" : "";
        let li2 = `<li onclick="updateSkinTone(this)" class="${isSelected2}">${SkinTone}</li>`;
        options2.insertAdjacentHTML("beforeend", li2);
    });
}
addSkinTone();

function updateSkinTone(selectedLi2) {
    
    addSkinTone(selectedLi2.innerText);
    wrapper2.classList.remove("active2");
    selectBtn2.firstElementChild.innerText = selectedLi2.innerText;
    finalSkinTone = selectedLi2.innerText;
}

selectBtn2.addEventListener("click", () => wrapper2.classList.toggle("active2"));


const wrapper3 = document.querySelector(".wrapper3"),
selectBtn3 = wrapper3.querySelector(".select-btn3"),
searchInp3 = wrapper3.querySelector("input3"),
options3 = wrapper3.querySelector(".options");

let Season = ["Summer", "Autumn", "Spring", "Winter"];

function addSeason(selectedSeason) {
    options3.innerHTML = "";
    Season.forEach(Season => {
        let isSelected3 = Season == selectedSeason ? "selected" : "";
        let li3 = `<li onclick="updateSeason(this)" class="${isSelected3}">${Season}</li>`;
        options3.insertAdjacentHTML("beforeend", li3);
    });
}
addSeason();

function updateSeason(selectedLi3) {
 
    addSeason(selectedLi3.innerText);
    wrapper3.classList.remove("active3");
    selectBtn3.firstElementChild.innerText = selectedLi3.innerText;
    finalSeason = selectedLi3.innerText;
}

selectBtn3.addEventListener("click", () => wrapper3.classList.toggle("active3"));

document.getElementById("gender").value = finalGender;
document.getElementById("age").value = finalAge;
document.getElementById("event").value = finalDressCode;
document.getElementById("skintone").value = finalSkinTone;
document.getElementById("season").value = finalSeason;

