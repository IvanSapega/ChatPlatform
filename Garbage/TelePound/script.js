var uname = document.getElementsByClassName("username");
var ddmenu = document.getElementsByClassName("dropdown");
var tds = document.getElementsByClassName("tbl");
var ddactive = false,
    createActive = false;
var create = document.getElementById("create");
var createO = document.getElementsByClassName("create")[0];
uname[0].onclick = function() {
    //console.log(ddactive);
    if (ddactive) {
        tds[0].style.display = "none";
        ddmenu[0].style.height = "0px";
        ddactive = false;

    } else {
        tds[0].style.display = "block";
        ddmenu[0].style.height = "75px";
        ddactive = true;
    }
}
create.onclick = function() {
    console.log("heh");
    if (createActive) {
        createO.style.display = "none";
        createO.style.height = "0px";
        createActive = false;

    } else {
        createO.style.display = "block";
        createO.style.height = "200px";
        createActive = true;
    }
}