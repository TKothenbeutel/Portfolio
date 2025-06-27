async function retreiveTrackCover(token, uri){
    const songID = uri.split(":").at(-1);
    const result = await fetch("https://api.spotify.com/v1/tracks/"+songID, {
        method: "GET", headers: { Authorization: `Bearer ${token}` }
    });

    const results = await result.json();
    return results.album.images.at(0).url;
}

export async function populateDuplicateChoice(token, song, artist, uri1, album1, ts1, count1, uri2, album2, ts2, count2){
    //Retreive covers
    const cover1 = retreiveTrackCover(token, uri1);
    const cover2 = retreiveTrackCover(token, uri2);

    //Populate middle section
    document.getElementById("dupSongName").textContent = song;
    document.getElementById("dupSongArtist").textContent = artist;

    //Populate song1 fields    
    document.getElementById("song1Cover").src = await cover1;
    document.getElementById("song1Album").textContent = album1;
    document.getElementById("song1First").textContent = ts1;
    document.getElementById("song1Count").textContent = count1;

    //Populate song2 fields
    document.getElementById("song2Cover").src = await cover2;
    document.getElementById("song2Album").textContent = album2;
    document.getElementById("song2First").textContent = ts2;
    document.getElementById("song2Count").textContent = count2;
}

export function toggleDupChoice(){
    var element = document.getElementById("dupSongChoice");
    if(element.style.display == "none"){
        element.style.display = "flex";
    }else{
        element.style.display = "none";
    }
}

function waitForResponse(){
    var option1 = document.getElementById("song1");
    var option2 = document.getElementById("song2");
    var both = document.getElementById("dupSongBoth");
    return new Promise(resolve => {
        option1.addEventListener("click", function handler(){
            resolve("song1");
        });
        option2.addEventListener("click", function handler(){
            resolve("song2");
        });
        both.addEventListener("click", function handler(){
            resolve("both");
        });
    });
}

export async function getChoice(){
    return await waitForResponse();
}



//import { retreiveToken } from './spotifyAccountRetreiver.js'
//const token = retreiveToken();
//populateDuplicateChoice(token,"RISK, RISK, RISK!","Jhariah",
//                                  "spotify:track:2FgFvtSuBAECcN7SJU5xMB","RISK, RISK, RISK!","2024-04-09",3,
//                                  "spotify:track:3ekN6ytJmlh5y93ChIqOtA","TRUST CEREMONY","2024-04-21",20
//                       );