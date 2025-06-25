#from pyodide.ffi import JsProxy
#from pyscript.js_modules import script as sc
import spotipy

#token = await sc.getToken()

#print(token)



# Create a Spotify API client using the access token
#sp = spotipy.Spotify(auth=token)

# Make an API call, for example, to get the current user's profile
#user_profile = sp.current_user()

#print("\n\nUSER INFO:")
#print(user_profile)

username = "kothenbeutel"
playlist = "idk"
URIs = [
    "spotify:track:4dRBLORJbxTdRKqMpygLSd",
    "spotify:track:7asyVbwQE7IbA3x2be7bdI",
    "spotify:track:7sL05OTVdmVcwsAG2IBf1G",
    "spotify:track:3ZEBra0Tn62AqkECRT3yEI"
]


#print("setting unavailable")

#sp.user_playlist_add_tracks(username, playlist, URIs)

#print("Songs added.")

#print(sc())
#print("PROFILE:",profile.as_py_json())

#print(type(jVar))

#print(jVar.to_py())

#if isinstance(jVar, JsProxy):
#    if jVar.constructor.name == "Array":
#        print(list(jVar))
#    print(dict(jVar))

#for(i in profile):
#    print(i)


#from pyscript.js_modules import settings as s
from pyodide.ffi.wrappers import add_event_listener
from pyscript.js_modules import fileReader
from pyscript.js_modules import settings

print(settings.disableInput("beginningDate"))


import json

#async def getData():
#    eep = json.loads(womp)
    
#fileBttn = document.querySelector("#fileComplete")
#fileBttn.add_event_listener("click", printFiles)


#while True:
#    if(not document.querySelector("#dataUpload").value == ""):
        #print(document.querySelector("#dataUpload").value)

        #print(fileReader.yarg)
        #await getData()
#        break
print("done")
#eep = s.disableInput("minCount")
#print(eep)

from pyscript.js_modules import spotifyJS
from pyscript.js_modules import sAccount


#spotifyJS.populateDuplicateChoice(sAccount.accessToken,"RISK, RISK, RISK!","Jhariah",
#                                  "spotify:track:2FgFvtSuBAECcN7SJU5xMB","RISK, RISK, RISK!","2024-04-09",3,
#                                  "spotify:track:3ekN6ytJmlh5y93ChIqOtA","TRUST CEREMONY","2024-04-21",20)

