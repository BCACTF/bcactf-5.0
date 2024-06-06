// bold all text that was searched for

for (let i of search.split(" ")) {
    for (let element of document.getElementsByClassName("result-text")) {
        element.innerHTML = element.innerHTML.replaceAll(i, "<b>" + i + "</b>");
    }
}
