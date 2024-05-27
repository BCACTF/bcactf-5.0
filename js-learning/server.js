const express = require("express");
const app = express();
const port = 3000;
const parser = require("body-parser");
const fs = require("fs");

app.use("/", express.static("static"));

app.use(parser.text());
app.get("/", (req, res) => {
    res.send("index.html");
});


app.post("/check", (req, res) => {
    let flag = fs.readFileSync("flag.txt", "utf-8");

    let d = req.body;
    let out = "";
    for (let i of ["[", "]", "(", ")", "+", "!"]) {
        d = d.replaceAll(i, "");
    }
    if (d.trim().length) {
        res.send("ERROR: disallowed characters. Valid characters: '[', ']', '(', ')', '+', and '!'.");
        return;
    }

    let c;
    try {
        c = eval(req.body).toString();
    } catch (e) {
        res.send("An error occurred with your code.");
    }

    // disallow code execution
    try {
        if (typeof (eval(c)) === "function") {
            res.send("Attempting to abuse javascript code against jslearning.site is not allowed under our terms and conditions.");
        }
    } catch (e) {}


    out += "Checking the string " + c + "...|";
    if (c === "fun") {
        out+='Congratulations! You win the level!';
    } else {
        out+="Unfortunately, you are incorrect. Try again.";
    }
    res.send(out);
});

app.listen(port, () => {});
console.log("Server started on http://localhost:" + port);