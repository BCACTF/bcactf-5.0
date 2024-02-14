var die1 = 0;
var die2 = 0;
var subtract = false;
let result = document.getElementById("result");
let input = document.getElementById("input");
let dicetext = document.getElementById("dicetext");
let img1 = document.getElementById("img1");
let img2 = document.getElementById("img2");
let resultbuttons = document.getElementsByClassName("resultbutton")

input.value = ""; 


input.onclick = () => { // can't turn off readonly now
    input.readOnly = true;
}
input.onchange = () => { // now you really can't edit it
    input.readOnly = true;
    input.value = "";
}
document.body.onkeydown = () => { // now you REALLY can't edit it
    input.readOnly = true;
}

function rollDice() {
    die1 = Math.floor(Math.random()*6)+1;
    die2 = Math.floor(Math.random()*6)+1;
    if (input.value === "123456789") { 
        die1 = 1;
        die2 = 1;
    } // lol
    img1.src = "./images/" + die1 + ".jpeg";
    img2.src = "./images/" + die2 + ".jpeg";    
    subtract = false;
    dicetext.innerHTML = "You rolled a " + die1 + " and a " + die2 + ", for a result of " + (subtract ? Math.abs(die1-die2) : (die1 + die2)) + "."
    for (let r of resultbuttons) r.style.display = "inline";
    if (1 == die1 == die2) {
        dicetext.innerHTML = "Snake eyes! Your input has been reset.";
        input.value = "";
        for (let r of resultbuttons) r.style.display = "none";
    }
    result.style.display = "inline";
    
}

function addNumber() {
    input.value += (subtract ? Math.abs(die1-die2) : die1+die2);
    result.style.display = "none";
}
function submit() {
    if (!input.value) {
        alert("Please enter a phone number.");
        return;
    }
    var c = confirm("Is " + input.value + " the correct phone number?");
    if (!c) return;
    if (input.value === "1234567890") fetch("flag.txt").then((res) => res.text()).then((text) => {
        document.body.innerHTML = text;
    });
}

function subtractSet() {
    subtract = true;
    dicetext.innerHTML = "You rolled a " + die1 + " and a " + die2 + ", for a result of " + (subtract ? Math.abs(die1-die2) : (die1 + die2)) + ".";
}
