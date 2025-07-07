"""File that tests the functionality and ensure it all works :)"""

"""File Reader"""
def fileReaderTest():
  from pyscript.js_modules import fileReader # type: ignore
  import json
  from os import system, name
  #1. Gray out sections
  #2. Get inputted files 
  #3. Move to next section
  #4. Show results for download
  sections = ["parsingFiles", "forceAddFiles", "forceRemoveFiles", "forceRemoveFiles"]
  for i in range(3):
    input("Enter when finished adding files.")
    fileReader.readOnlySection(sections[i]) #Gray out
    files = fileReader.filesToPy().to_py() #Get files
    files[0][1] = json.loads(files[0][1])
    print("Files:\n",files[0][0])
    print(type(files[0]))
    fileReader.updateFileInputSection(sections[i+1]) #Open next section
  #Gray out last one again
  fileReader.readOnlySection(sections[-1])
  #Show download
  fileReader.displayResults("test.json")
  return True

"""Settings"""
def settingsTest():
  from pyscript.js_modules import settings # type: ignore
  #Retreive setting value, which then disables input for that setting
  selectNames = [
    "beginningDate",
    "minMS",
    "songPreference",
    "playlistAddTimer",
    "songGracePeriod",
    "universalMinCount",
  ]
  for i in selectNames:
    input("Retreiving setting " + i)
    setting = settings.getSetting(i)
    print("\t",setting)
  return True

"""spotifyAccountRetreiver"""
def runSAcc():
  import asyncio
  #Helper for the async stuff
  loop = asyncio.get_event_loop()
  loop.run_until_complete(loop.create_task(sAccountTest()))
  loop.close()
  return True


async def sAccountTest():
  from pyscript.js_modules import sAccount # type: ignore
  #1. Prompt to sign in
  #2. Get already retreived access token
  #3. Get user info
  test = [1,2,3,4]
  input("Ready for sign in:")
  token1 = await sAccount.retreiveToken(test)
  print("Token function:",token1)
  if(token1):
    print("Saved:",sAccount.getPrevRes())
  token2 = await sAccount.retreiveToken(None)
  print("Token variable:",token2)
  if(token2):
    print("No saved",sAccount.getPrevRes())
  accInfo = sAccount.retreiveUser()
  print("Account\n",accInfo)
  return token1

"""spotifyApi"""
def runSpotify():
  import asyncio
  #Helper for the async stuff
  loop = asyncio.new_event_loop()
  loop.run_until_complete(loop.create_task(spotifyJSTest()))
  loop.close()
  return True

async def spotifyJSTest():
  from pyscript.js_modules import spotifyJS # type: ignore
  #Get authorization token
  token = await sAccountTest()
  #1. Enable duplicate choice
  #2. Populate duplicate choice
  #3. Get choice
  #4. Disable duplicate choice
  spotifyJS.toggleDupChoice()
  spotifyJS.populateDuplicateChoice(
    token,"RISK, RISK, RISK!","Jhariah",
    "spotify:track:2FgFvtSuBAECcN7SJU5xMB","RISK, RISK, RISK!","2024-04-09",3,
    "spotify:track:3ekN6ytJmlh5y93ChIqOtA","TRUST CEREMONY","2024-04-21",20
  )
  choice = await spotifyJS.getChoice()
  print("Choice made:",choice)
  spotifyJS.populateDuplicateChoice(
    token,"Ballerina","Daisy the Great",
    "spotify:track:1ctY8BRqB4b9VB2beSyhz7","Ballerina","2023-12-10",500,
    "spotify:track:3glDaGn3UGafxzC6jqroZd","The Rubber Teeth Talk","2024-06-27",0
  )
  choice = await spotifyJS.getChoice()
  print("Choice made:",choice)
  spotifyJS.populateDuplicateChoice(
    token,"Big Town Banky Blaine's Rockabilly BBQ","Bear Ghost",
    "spotify:track:2QyKgIbQmuyzFIE65NQJne","Big Town Banky Blaine's Rockabilly BBQ","2022-06-17",5,
    "spotify:track:5xqNQ99qlWabj14s8s7eBF","Jiminy","2023-09-30",40
  )
  choice = await spotifyJS.getChoice()
  print("Choice made:",choice)
  spotifyJS.toggleDupChoice()
  return True

"""Helpers"""
def helpersTest():
  from pyscript.js_modules import settings # type: ignore

"""spotifyApi"""
def runUpload():
  import asyncio
  #Helper for the async stuff
  loop = asyncio.new_event_loop()
  loop.run_until_complete(loop.create_task(uploadToSpotify()))
  loop.close()
  return True

async def uploadToSpotify():
  from pyscript.js_modules import sAccount # type: ignore
  from pyscript.js_modules import spotifyJS # type: ignore
  accessToken = await sAccount.retreiveToken()
  #1. See if playlist is editable
  #2. Add songs to playlist if so
  playlist = "7L40apfN820LogCSpfMmjp"
  URIs = [
      "spotify:track:4dRBLORJbxTdRKqMpygLSd",
      "spotify:track:7asyVbwQE7IbA3x2be7bdI",
      "spotify:track:7sL05OTVdmVcwsAG2IBf1G",
      "spotify:track:3ZEBra0Tn62AqkECRT3yEI"
  ]
  #Check if playlist is editable
  try:
    if(await spotifyJS.isEditablePlaylist(accessToken,playlist,"kothenbeutel")):
      print("Adding songs to Playlist")
      #res = await spotifyJS.addSongs(accessToken, playlist, URIs)
      #print("Added songs ",res)
      #tracks = (await spotifyJS.retreiveTracks(accessToken, playlist)).to_py()
      #print(tracks)
    else:
      print("Playlist is not editable")
    return True
  except Exception as e:
    if(str(e) == "Error: 404"):
      print("Not a valid playlist ID.")
    else:
      print(e)

if __name__ == "__main__":
  #fileReaderTest()
  settingsTest()
  #runSAcc()
  #runSpotify()
  #helpersTest()
  #runUpload()
  print("All tests passed!")
