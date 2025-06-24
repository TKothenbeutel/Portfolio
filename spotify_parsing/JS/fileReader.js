var sectionID = "parsingFiles" // or forceAddFiles or forceRemoveFiles
var readers = [];
var fileKeys = [];
var fKey = 20;

document.getElementById("fileBox").addEventListener("drop", function (ev) {
    ev.preventDefault();
    const files = [];
    if (ev.dataTransfer.items) {
        [...ev.dataTransfer.items].forEach((item, i) => {
            if (item.kind === "file" && item.type === "application/json") {
                const file = item.getAsFile();
                files.push(file);
            }
        });
    } else {
        [...ev.dataTransfer.files].forEach((file, i) => {
            files.push(file);
        });
    }
    saveFiles(files);
});

document.getElementById("fileBox").addEventListener("dragover", function (ev) {
    ev.preventDefault();
});

document.getElementById("dataUpload").addEventListener("change",function () {
    saveFiles(this.files);   
});

function saveFiles(files){
    for(let i = 0; i < files.length; i++){
        var reader = new FileReader();
        reader.readAsText(files[i]);
        fKey++;
        readers.push(reader);
        fileKeys.push(fKey); 
        makeFileNotifier(files[i].name, fKey);
    }
}

function makeFileNotifier(fileName, index){
    var copied = document.getElementsByClassName("fileImported")[0];
    var copy = copied.cloneNode(true);
    document.getElementById(sectionID).appendChild(copy);
    copy.removeAttribute('hidden');
    copy.children[1].textContent = "\u00A0\u00A0\u00A0Imported\u00A0\u00A0\u00A0" + fileName;
    var bttn = copy.children[0];
    bttn.value = index;
    bttn.addEventListener("click",function(){
        var fIndex = fileKeys.indexOf(parseInt(this.value));
        readers.splice(fIndex, 1);
        fileKeys.splice(fIndex, 1);
        this.parentElement.remove();
    });
}


export function readOnlySection(section){
    var section = document.getElementById(section);
    for(const child of section.children){
        if(child.tagName == "LABEL"){
            child.style.color = "#595959";
        }else{
            child.style.borderColor = "#7f7f7f";
            child.style.backgroundColor = "#b8b8b8";
            child.children[0].hidden = true;
        }
    }
}

export function filesToPy(){
    var files = [];
    for(let i = 0; i < readers.length; i++){
        files.push(readers[i].result);
    }
    return files;
}

export function updateFileInputSection(area){
    sectionID = area;
    readers = [];
    fileKeys = [];
    document.getElementById(sectionID).hidden = false;
}
