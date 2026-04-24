//Displays notice message at bottom until closed out, to which it won't show again while the cookies are there

function noticeLogic(){
    //
    if(localStorage.getItem("noticed") != "True"){
        document.getElementById("notice").style.display = "flex";
        document.getElementById("closeButton").onclick = (event) => {
            localStorage.setItem("noticed", "True");
            document.getElementById("notice").style.display = "none";
        }
    }
}

window.onload = function () {
    noticeLogic();
};