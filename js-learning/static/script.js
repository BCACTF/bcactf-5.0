let code = document.getElementById("code");
async function check() {
    await fetch('/check', {
        method:'POST',
        body: code.innerText
    }).then((res)=>res.text()).then((text)=>alert(text))
}