const redirect_uri = "http://127.0.0.1:3000/_posts/spotify-song-parser.html";
const clientId = "2bad936b5dec4ee286a3bed50cbb9a57";
const params = new URLSearchParams(window.location.search);
const code = params.get("code");
var accessToken = "";
if(code){
    getToken();
}else{
    document.getElementById("loggedInText").hidden = true;
}
document.getElementById("spotifySignIn").addEventListener("click",getToken);
document.getElementById("signOutButton").onclick = function(){
    localStorage.removeItem("verifier");
    localStorage.removeItem("refresh_token");
    document.location = redirect_uri;
};

export async function getSpotifyUser(){
    if(accessToken == ""){
        await getToken();
        var profile = await fetchProfile(accessToken);
        return (accessToken, profile);
    }else{
        var profile = await fetchProfile(accessToken);
        return [accessToken, profile];
    }
}

export async function retreiveToken(){
    if(accessToken == ""){
        return await getToken();
    }else{
        return accessToken;
    }
}

async function getToken(){
    if (!code) {
        return redirectToAuthCodeFlow(clientId);
    } else {
        accessToken = await getAccessToken(clientId, code);
        const profile = await fetchProfile(accessToken);
        populateUI(profile);
        return accessToken;
    }
}

async function redirectToAuthCodeFlow(clientId) {
    const verifier = generateCodeVerifier(128);
    const challenge = await generateCodeChallenge(verifier);

    localStorage.setItem("verifier", verifier);

    const params = new URLSearchParams();
    params.append("client_id", clientId);
    params.append("response_type", "code");
    params.append("redirect_uri", redirect_uri);
    params.append("scope", "user-read-private user-read-email user-library-read playlist-modify-private playlist-modify-public");
    params.append("code_challenge_method", "S256");
    params.append("code_challenge", challenge);

    document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
}

async function getAccessToken(clientId, code) {
    const verifier = localStorage.getItem("verifier");

    const params = new URLSearchParams();
    params.append("client_id", clientId);
    params.append("grant_type", "authorization_code");
    params.append("code", code);
    params.append("redirect_uri", redirect_uri);
    params.append("code_verifier", verifier);

    const result = await fetch("https://accounts.spotify.com/api/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params
    });

    const response = await result.json();

    if(response.error){
        return getRefreshToken(clientId);
    }

    localStorage.setItem("refresh_token", response.refresh_token);

    const access_token = response.access_token;
    return access_token;
}

export async function getRefreshToken(clientId) {
    const refresh_token = localStorage.getItem("refresh_token");
    if(!refresh_token){
        throw new Error("Refresh token doesn't exist.");
    }

    const params = new URLSearchParams();
    params.append("grant_type", 'refresh_token');
    params.append("refresh_token", refresh_token);
    params.append("client_id", clientId);

    const result = await fetch("https://accounts.spotify.com/api/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params
    });

    const response = await result.json();

    if (response.refresh_token) {
      localStorage.setItem('refresh_token', response.refresh_token);
    }

    const access_token = response.access_token;
    return access_token;
}

function generateCodeVerifier(length) {
    let text = '';
    let possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    for (let i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

async function generateCodeChallenge(codeVerifier) {
    const data = new TextEncoder().encode(codeVerifier);
    const digest = await window.crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode.apply(null, [...new Uint8Array(digest)]))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}

async function fetchProfile(code){
    const result = await fetch("https://api.spotify.com/v1/me", {
        method: "GET", headers: { Authorization: `Bearer ${code}` }
    });

    return await result.json();
}

function populateUI(profile) {
    document.getElementById("spotifySignIn").hidden = true;
    document.getElementById("loggedInText").hidden = false;
    document.getElementById("displayName").innerText = profile.display_name;
    document.getElementById("spotifyId").innerText = profile.id;
}

