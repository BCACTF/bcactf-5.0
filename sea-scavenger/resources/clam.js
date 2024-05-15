document.cookie = "flag part 3:=1dnt_f";

window.onbeforeunload = function() {
    // Your cleanup code here
    document.cookie = "flag part 3:=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
};  