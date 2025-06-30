#from os import system, name
#from os.path import abspath
#from datetime import datetime
#import Environment_Variables
#import helpers.Settings as S
#from helpers.Formatting import *
#from helpers.DataParse import validatedFile, dictToJSON, validatedFolder
#from helpers.SongStruct import MasterSongContainer
#from helpers.ProgressBar import ProgressBar
#from helpers.SpotifyFunctions import SpotifyGateway

import asyncio
from datetime import datetime
from helpers.Formatting import *
from helpers.DataParse import validatedFile, dictToJSON, validatedFolder
from helpers.SpotifyFunctions import SpotifyGateway
from helpers.SongStruct import MasterSongContainer

from pyscript.js_modules import sAccount
from pyscript.js_modules import fileReader


def currentTime():
  return f'{datetime.today().date()}_{str(datetime.today().time()).replace(":","-")[:8]}'

def runAsync(task):
  loop = asyncio.get_event_loop()
  res = loop.run_until_complete(task)
  return res

async def populateSpotipy():
  token = (await sAccount.getSpotifyUser()).to_py()
  playlist = input("Playlist = ")
  sp = SpotifyGateway(token[0],token[1]['id'],playlist)
  if(not sp.validateInformation()):
    input("Fail")
    return populateSpotipy()
  print("pass")

def saveResults(songContainer: MasterSongContainer):
  plainSongs = {} #Get dictionary in a readable format
  for key in songContainer.desiredSongs:
    value = songContainer.desiredSongs[key]
    plainSongs[key] = {
      "timestamp":str(value.ts),
      "title":value.title,
      "artist":value.artist,
      "album":value.album,
      "count":value.count
    }
  fPath = f"./results.json"
  resultToJSON = dictToJSON(plainSongs)
  with open(fPath,'w') as file:
    file.write(resultToJSON)
  name = f'{currentTime()}.json'
  fileReader.displayResults(name)

async def addToPlaylist(songContainer:MasterSongContainer):

  token = (await sAccount.getSpotifyUser()).to_py()
  if(token[0] == "None"): #or is it false basically
    print("NO USER DETECTED.")

  print(f'\nTo add these songs onto a playlist, some information of your {bold("Spotify")} is first needed.')

  playlist_id = input(f"Now, please enter the ID of the playlist you would like the songs added to. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID: ")
  if(playlist_id.lower() == 'help' or playlist_id.lower() == 'h'):
    print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
    playlist_id = input("Please enter the desired playlist's id: ")
  
  sp = SpotifyGateway(token[0],token[1]['id'],playlist_id)

  print('Now testing to ensure the playlist can be editable.')
  test = sp.validateInformation()
  if(not test): #Test failed
    print(f'Unfortunately, the test was unsuccessful. Please keep in mind to enter your {bold("username")} and a {bold("playlist ID")} that you are the owner of.')
    input(f'Press {bold("Enter")} to try again.\n')
    return addToPlaylist(songContainer)
  #Test passed
  print()
  print("Test has successfully passed. Now it's time to add the songs to the playlist.\n")
  input()#Wait for user

  #If timer is >0, run timed adder
  if(S.settingByName('playlistAddTimer').value > 0):
    sp.addToSpotifyTimed(songContainer.desiredSongs,S.settingByName('playlistAddTimer').value)
  #Else run batch adder
  else:
    sp.addToSpotifyBatch(songContainer.desiredSongs)
  print('All songs successfully added to the playlist.')
  input()
  return