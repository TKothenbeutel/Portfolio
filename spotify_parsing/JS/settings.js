var today = new Date();
var lastYear = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());
var prevWeek = new Date(today);
prevWeek.setDate(today.getDate() - 7);
var tomorrow = new Date(today);
tomorrow.setDate(today.getDate() + 1);
var defaultVals = [
    ["beginningDate",dateToString(lastYear)],
    ["minCount","2"],
    ["minMS","30000"],
    ["songPreference","ask"],
    ["minCountOverride","-1"],
    ["earliestDate","2000-01-01"],
    ["lastDate",dateToString(tomorrow)],
    ["playlistAddTimer","0.00"],
    ["songGracePeriod",dateToString(prevWeek)],
    ["universalMinCount","false"]
];

function inputChanged() {
    if(this.value == ''){//Prevent empty value
        this.value = localStorage.getItem(this.id);
    }else{
        localStorage.setItem(this.id,this.value);
    }
    
}
function toDefault(){
    for(var i = 0; i < defaultVals.length; i++){
        console.log(defaultVals[i]);
        console.log(defaultVals[i][0], defaultVals[i][1]);
        localStorage.setItem(defaultVals[i][0],defaultVals[i][1]);
        document.getElementById(defaultVals[i][0]).value = defaultVals[i][1];
    }
    const songPrefID = localStorage.getItem("songPreference");
    document.getElementById(songPrefID).checked = true;
    document.getElementById("universalMinCount").checked =
            localStorage.getItem("universalMinCount") == "true";
    console.log(document.getElementById("universalMinCount").checked);
}

function dateToString(date) {
    var year = date.getFullYear();
    var month = ("0" + (date.getMonth() + 1)).slice(-2);
    var day = ("0" + date.getDate()).slice(-2);
    return "".concat(year, "-").concat(month, "-").concat(day);
}
function updateAllSettings() {
    for(var i = 0; i < defaultVals.length; i++){
        document.getElementById(defaultVals[i][0]).value =
            localStorage.getItem(defaultVals[i][0]);
    }
    const songPrefID = localStorage.getItem("songPreference");
    document.getElementById(songPrefID).checked = true;
    document.getElementById("universalMinCount").checked =
            localStorage.getItem("universalMinCount") == "true";
}

export function disableInput(elementID){
    inp = document.getElementById(elementID);
    inp.readOnly = true;
    return (inp.type == "checkbox") ? inp.checked : inp.value;
}

window.onload = function () {
    if(localStorage.getItem("minCount") == null){
        toDefault();
    }else{
        updateAllSettings();
    }
    
    //Setting up reset button
    document.getElementById("resetSettings")
        .addEventListener("click", toDefault);
    
    // Setting HTML onChange function
    /// Dates
    document.getElementById("beginningDate")
        .addEventListener("change",inputChanged);
    document.getElementById("earliestDate")
        .addEventListener("change",inputChanged);
    document.getElementById("lastDate")
        .addEventListener("change",inputChanged);
    document.getElementById("songGracePeriod")
        .addEventListener("change",inputChanged);
    /// Numbers
    document.getElementById("minCount")
        .addEventListener("change",inputChanged);
    document.getElementById("minMS")
        .addEventListener("change",inputChanged);
    document.getElementById("minCountOverride")
        .addEventListener("change",inputChanged);
    document.getElementById("playlistAddTimer")
        .addEventListener("change",inputChanged);
    /// Options
    document.getElementById("oldest")
        .addEventListener("click",(event)=>{
            localStorage.setItem("songPreference",event.currentTarget.id);
        });
    document.getElementById("newest")
        .addEventListener("click",(event)=>{
            localStorage.setItem("songPreference",event.currentTarget.id);
        });
    document.getElementById("both")
        .addEventListener("click",(event)=>{
            localStorage.setItem("songPreference",event.currentTarget.id);
        });
    document.getElementById("ask")
        .addEventListener("click",(event)=>{
            localStorage.setItem("songPreference",event.currentTarget.id);
        });
    //Checkbox
    document.getElementById("universalMinCount")
        .addEventListener("change",(event)=>{
            localStorage.setItem(event.currentTarget.id,event.currentTarget.checked);
        });
};
