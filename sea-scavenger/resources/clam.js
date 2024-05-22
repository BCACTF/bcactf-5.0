document.cookie = "flag part 3:=dnt_f1n";

window.onbeforeunload = function() {
    // Your cleanup code here
    document.cookie = "flag part 3:=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
};  