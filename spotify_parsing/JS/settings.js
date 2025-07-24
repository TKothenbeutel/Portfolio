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
function choiceEvent(event){
    localStorage.setItem("songPreference",event.currentTarget.id);
}

function toDefault(){
    for(var i = 0; i < defaultVals.length; i++){
        var setting = document.getElementById(defaultVals[i][0])
        console.log(setting.disabled);
        if(setting.disabled == false){
            localStorage.setItem(defaultVals[i][0],defaultVals[i][1]);
            setting.value = defaultVals[i][1];
        }
    }
    if(!document.getElementById("songPreference").children.item(0).disabled){
        localStorage.setItem(defaultVals[3][0],defaultVals[3][1]);
        document.getElementById(defaultVals[3][1]).checked = true;
    }
    if(!document.getElementById("universalMinCount").disabled){
        document.getElementById("universalMinCount").checked =
            localStorage.getItem("universalMinCount") == "true";
    }
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

export function getSetting(elementID){
    var inp = document.getElementById(elementID);
    if(inp.tagName == "DIV"){   //case for songPreferences (collection of buttons)
        for(const child of inp.children){
            if(child.tagName == "INPUT"){
                child.disabled = true;
                child.removeEventListener("click",choiceEvent);
            }else if(child.tagName == "LABEL"){
                if(child.htmlFor == localStorage.getItem(elementID)){
                    child.style.backgroundColor = "#66807c";
                    child.style.textShadow = "none";
                    child.style.color = "#3b3b3b";
                }else{
                    child.style.backgroundColor = "#d1d1d1";
                    child.style.color = "#6d6d6d";
                }
                child.style.cursor = "default";
            }
        }
    }else{
        inp.disabled = true;
    }
    return localStorage.getItem(elementID);
    //return (inp.type == "checkbox") ? inp.checked : inp.value;
}

export function unBlockSetting(elementID){
    var inp = document.getElementById(elementID);
    if(inp.tagName == "DIV"){   //case for songPreferences (collection of buttons)
        for(const child of inp.children){
            if(child.tagName == "INPUT"){
                child.disabled = false;
                child.addEventListener("click",choiceEvent);
            }else if(child.tagName == "LABEL"){
                if(child.htmlFor == localStorage.getItem(elementID)){
                    child.style.backgroundColor = "#aafdf2";
                    child.style.textShadow = "0px 0px 1px black";
                    child.style.color = "#000000";
                }else{
                    child.style.backgroundColor = "#ffffff";
                    child.style.color = "#000000";
                }
                child.style.cursor = "pointer";
            }
        }
    }else{
        inp.disabled = false;
    }
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
        .addEventListener("click",choiceEvent);
    document.getElementById("newest")
        .addEventListener("click",choiceEvent);
    document.getElementById("both")
        .addEventListener("click",choiceEvent);
    document.getElementById("ask")
        .addEventListener("click",choiceEvent);
    //Checkbox
    document.getElementById("universalMinCount")
        .addEventListener("change",(event)=>{
            localStorage.setItem(event.currentTarget.id,event.currentTarget.checked);
    });
};
