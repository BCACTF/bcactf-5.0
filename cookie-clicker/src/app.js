const express = require('express')
const app = express();

const http = require('http').Server(app);

const port = 3000;

const socketIo = require('socket.io');
const io = socketIo(http);

const { v4 } = require('uuid');

let sessions = {}
let errors = {}

app.use(express.static(__dirname));

app.get('/', (req, res) => {
    res.sendFile("./index.html")
})

io.on('connection', (socket) => {
    let id = v4();
    sessions[id] = 0
    errors[id] = 0

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });

    socket.on('chat message', (msg) => {
        io.emit('chat message', msg);
    });

    socket.on('receivedError', (msg) => {
        sessions[id] = errors[id]
        io.emit('recievedScore', JSON.stringify({"value":sessions[id]}));
    });

    socket.on('click', (msg) => {
        let json = JSON.parse(msg)

        if (sessions[id] > 1e7) {
            console.log("TEST")
            io.emit('recievedScore', JSON.stringify({"value":"bcactf{Y0u_W3renT_Supp0sE_t0_WIN_123}"}));
            return;
        }

        if (json.value != sessions[id]) {
            io.emit("error", "previous value does not match")
        }

        let oldValue = sessions[id]
        let newValue = Math.floor(Math.random() * json.power) + 1 + oldValue

        sessions[id] = newValue
        io.emit('recievedScore', JSON.stringify({"value":newValue}));

        if (json.power > 100) {
            io.emit('error', JSON.stringify({"value":oldValue}));
        }

        errors[id] = oldValue;
    });
});

http.listen(port, () => {
    console.log(`App server listening on ${port}. (Go to http://localhost:${port})`);
});