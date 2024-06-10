// your value is only updated server-side when the client
// acknowledges an error by sending the receivedError event
// so you can just disable this

// paste this into the JS console

socket.off('error');
socket.emit('click', JSON.stringify({"power":1e100, "value":send.value}));
socket.emit('click', JSON.stringify({"power":1e100, "value":send.value}));

// (you have to send it twice since it only updates 
// once the already-stored point value on the server side is
// more than 1e20)