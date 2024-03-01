const express = require("express");
const app = express();
const port = 3000;
const parser = require("body-parser");


const flag = "bcactf{1ava5cRIPT_mAk35_S3Nse_48129846}";


app.use("/", express.static("static"));

app.use(parser.text());
app.get("/", (req, res) => {
    res.send("index.html");
});


app.post("/check", (req, res) => {
    let d = req.body;
    for (let i of ["[", "]", "(", ")", "+", "!"]) {
        d = d.replaceAll(i, "");
    }
    if (d.trim().length) {
        res.send("ERROR: disallowed characters. Valid characters: '[', ']', '(', ')', '+', and '!'.");
        return;
    }

    if (eval(req.body) === "fun") {
        res.send('Congratulations! You win the level!');
    } else {
        res.send("Unfortunately, you are incorrect. Try again.");
    }
});
app.listen(port, () => {});