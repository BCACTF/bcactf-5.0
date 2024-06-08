var socket = io();

let cookie = document.querySelector("img")

class sendMessage {
    power = 1
    value = 0
}

let send = new sendMessage();

cookie.addEventListener('click', function (e) {
    socket.emit('click', JSON.stringify({"power":send.power, "value":send.value}));
});

socket.on('recievedScore', function (msg) {
    let scores = JSON.parse(msg)
    send.value = scores.value
    document.querySelector(".points").textContent = scores.value
});

socket.on('error', function (msg) {
    console.log("Error")
    socket.emit('receivedError', "recieved");
});