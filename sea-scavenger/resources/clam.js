document.cookie = "flag part 3:=dnt_f1n";

window.onbeforeunload = function() {
    document.cookie = "flag part 3:=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
};  

console.log("Hint: how do websites remember you? Where do websites store things?")
