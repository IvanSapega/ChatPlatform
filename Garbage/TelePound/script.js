var uname = document.getElementsByClassName("username");
var ddmenu = document.getElementsByClassName("dropdown");
var tds = document.getElementsByClassName("tbl");
var ddactive = false;
uname[0].onclick = function() {
    //console.log(ddactive);
    if (ddactive) {
        tds[0].style.display = "none";
        ddmenu[0].style.height = "0px";
        ddactive = false;

    } else {
        tds[0].style.display = "block";
        ddmenu[0].style.height = "50px";
        ddactive = true;
    }
}