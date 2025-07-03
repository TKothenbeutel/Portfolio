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

from os import system
import asyncio
from datetime import datetime
from helpers.Formatting import *
from helpers.DataParse import validatedFile, dictToJSON, validatedFolder
from helpers.SpotifyFunctions import SpotifyGateway
from helpers.SongStruct import MasterSongContainer

from pyscript.js_modules import sAccount # type: ignore
from pyscript.js_modules import fileReader # type: ignore
from pyscript.js_modules import spotifyJS # type: ignore
from helpers.ProgressBar import ProgressBar

def currentTime():
  return f'{datetime.today().date()}_{str(datetime.today().time()).replace(":","-")[:8]}'

def runAsync(task):
  loop = asyncio.get_event_loop()
  res = loop.run_until_complete(task)
  return res

""" No Spotipy usage
async def populateSpotipy():
  token = (await sAccount.getSpotifyUser()).to_py()
  playlist = input("Playlist = ")
  sp = SpotifyGateway(token[0],token[1]['id'],playlist)
  if(not sp.validateInformation()):
    input("Fail")
    return populateSpotipy()
  print("pass")
"""

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
  token = await sAccount.retreiveToken((songContainer.desiredSongs,"Addto"))
  user = sAccount.retreiveUser()
  print(f'\nTo add these songs onto a playlist, some information of your {bold("Spotify")} is first needed.')

  playlist_id = input(f"Now, please enter the ID of the playlist you would like the songs added to. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID: ")
  if(playlist_id.lower() == 'help' or playlist_id.lower() == 'h'):
    print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
    playlist_id = input("Please enter the desired playlist's id: ")

  print('Now testing to ensure the playlist can be editable.')
  try:
    if(not await spotifyJS.isEditablePlaylist(token,playlist_id,user)):
      print(f'Unfortunately, the test was unsuccessful. Please keep in mind to enter a {bold("playlist ID")} that you are the owner of.')
      input(f'Press {bold("Enter")} to try again.\n')
      return addToPlaylist(songContainer)
  except Exception as e:
    if(str(e) == "Error: 404"):
      input("The given input is not a valid playlist ID. Please try again.")
      return addToPlaylist(songContainer)
  #Test passed
  print()
  print("Test has successfully passed. Now it's time to add the songs to the playlist.\n")
  input()#Wait for user

  #TODO
  #If timer is >0, run timed adder
  if(S.settingByName('playlistAddTimer').value > 0):
    sp.addToSpotifyTimed(songContainer.desiredSongs,S.settingByName('playlistAddTimer').value)
  #Else run batch adder
  else:
    sp.addToSpotifyBatch(songContainer.desiredSongs)
  print('All songs successfully added to the playlist.')
  input()
  return

async def forceAdd(songContainer:MasterSongContainer) -> bool:
  """Asks user if they would like to force add/remove songs. Returns True if they did do either."""
  containerAltered = False
  __terminal__.clear() # type: ignore

  #Force add
  inp = input(f"I'm sure you got some great songs snagged already, but would you like any songs forced in the collection, regardless of the song's uniqueness? {bold('(y/n)')} ").lower()
  if(not(inp == 'y' or inp == 'yes')):
    if(inp == 'n' or inp == 'no'):
      return forceRemove(songContainer)
    else:
      print("Input could not be used. Please try again." )
      input()
      return forceAdd(songContainer)

  fileReader.updateFileInputSection("forceAddFiles") #Open section
  print("Sounds good! Please note that the timestamp added to these songs will be today's date and current time. If you save your song results, the songs added via this method will have a count of 0.")
  print()#Spacer

  token = sAccount.accessToken
  if(token == ""):
    inp = input("Before we begin, do you plan on adding songs via a Spotify playlist? (y/n) ").lower()
    while(not inp in ["n","no","y","yes"]):
      print("Input could not be read.")
      inp = input("Before we begin, do you plan on adding songs via a Spotify playlist? (y/n) ").lower()
    if(inp == "y" or inp == "yes"):
      input("To do so, you must be signed into your Spotify account through this program. The program will now direct you to Spotify's login page.")
      await sAccount.retreiveToken((songContainer.desiredSongs,"forceAdd"))

  songs = {}

  while(True):
    inp = ""
    if(token): #Spotify connected
      inp = input(f"Please enter the ID of the playlist or input any JSON files below that contain Spotify song URIs (in the format of the streaming history file). Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID. Enter {bold(underline('d')+'one')} when you are finished inputting playlist IDs and files, or enter {bold(underline('c')+'ancel')} if you would not like to add songs: ")
      print()#Spacer
      if(inp.lower() == 'help' or inp.lower() == 'h'):
        print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
        inp = input("Please enter the desired playlist's id: ")
        print()#Spacer
      if(inp.lower() == 'done' or inp.lower() == 'd'):
        break
      elif(inp.lower() == 'cancel' or inp.lower() == 'c'):
        songs = {}
        break
      elif(len(inp) == 22):#Playlist ID
        track_results = (await spotifyJS.retreiveTracks(token, inp)).to_py()
        if(track_results is None):
          print("The input could not be used. This could mean that the playlist given is empty or could not be found. Remember to enter an item one at a time. Please try again.")
          input()#Wait for user
          continue
        for song in track_results:
          songs[song['track']['uri']] = {
            'title' : song['track']['name'],
            'artist' : song['track']['artists'][0]['name'],
            'album' : song['track']['album']['name']
          }
        print(f"Found {len(track_results)} songs from this playlist.")
        input()#Wait for user
      else:
        print("Input could not be used. Please try again.")
        input()#Wait for user
        continue

    else: #Spotify not connected
      inp = input(f"Please enter JSON files containing Spotify song URIs (in the format of the streaming history file) that you would like to be included below. When finished, enter {bold(underline('d')+'one')}, or enter {bold(underline('c')+'ancel')} if you would not like to add songs: ")
      print()#Spacer
      if(inp.lower() == 'done' or inp.lower() == 'd'):
        break
      elif(inp.lower() == 'cancel' or inp.lower() == 'c'):
        songs = {}
        break
      else:
        print("Input could not be used. Please try again.")
        input()#Wait for user
        continue

  #Check for any inputted files
  fileReader.readOnlySection("forceAddFiles") #Gray out
  files = fileReader.filesToPy().to_py() #Get files
  if(files):
    for file in files:
      try:
        fileRes = validatedFile(file[1])
        if(type(fileRes) == dict): #Program's JSON
          for uri in fileRes:
            songs[uri] = fileRes[uri]
          print(f"Found {len(fileRes)} songs from this file.")
          input()#Wait for user
        elif(type(fileRes) == list): #Spotify's JSON
          for song in fileRes:
            songs[song['spotify_track_uri']] = {
              'title' : song['master_metadata_track_name'],
              'artist' : song['master_metadata_album_artist_name'],
              'album' : song['master_metadata_album_album_name']
            }
          print(f"Found {len(fileRes)} songs from this file.")
          input()#Wait for user
      except:
        while(True):
          inp = input(f"Could not use {files[0]}. Would you like to restart the force add process? (y/n) ")
          if(inp.lower() == "n" or inp.lower() == "no"):
            break
          elif(inp.lower() == "y" or inp.lower() == "yes"):
            return forceAdd(songContainer)
          else:
            print("Input could not be read. Please try again.")
  
  if(len(songs)>0):
    print("Time to add these songs to the collection!")
    input()
    pBar = ProgressBar(len(songs), 'Adding songs to collection')
    for uri in songs:
      if(uri in songContainer.desiredSongs):
        pBar.updateProgress() #Song already in collection
      else:
        containerAltered = True
        songContainer.forceAdd(uri, songs[uri]['title'], songs[uri]['artist'], songs[uri]['album'])
        pBar.updateProgress()
    pBar.finish()
    print(f"Your new total is now {bold(len(songContainer.desiredSongs))} songs!")
    input()#Wait for user
    __terminal__.clear() # type: ignore
  return forceRemove(songContainer)
  












#TODO: Fix forceRemove and add option to list songs by given artist

def forceRemove(songContainer:MasterSongContainer) -> bool:
  #Force remove
  while(True):#While loop in case input could not be read
    inp = input(f"Would you like to force remove any songs from this collection? {bold('(y/n)')} ").lower()
    
    if(inp == 'y' or inp == 'yes'):
      print("Sounds good!")
      print()#Spacer

      sp = SpotifyGateway(None, None)
      songs = []
      print("If you enter a playlist ID, the program may take you to a new tab with a broken webpage. This is normal. This tab builds the connection between this program and Spotify. What you will need to do is to copy the URL and paste it into the terminal when asked. Feel free to close the tab afterward.")
      print("If you have done this step before, this step will be omitted.")
      input()
      while(True):
        print(f"Please enter any of the following to remove included songs from the collection:")
        print(f"   * Spotify playlist ID\n   * JSON absolute file path (Spotify's streaming history file or previous results)\n   * Artist name (case-sensitive)\n   * Song title/URI")
        inp = input(f"Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID. Enter {bold(underline('d')+'one')} when you are finished inputting items for removal, or enter {bold(underline('c')+'ancel')} if you would not like to remove any songs: ")
        print()#Spacer
        if(inp.lower() == 'help' or inp.lower() == 'h'):
          print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
          inp = input("Please enter the desired playlist's ID, artist name, or song title: ").lower()
          print()#Spacer
        if(inp.lower() == 'done' or inp.lower() == 'd'):
          break
        elif(inp.lower() == 'cancel' or inp.lower() == 'c'):
          songs = []
          break
        else:#Input of artist/song/playlist
          artistResult = list(songContainer.desiredSongs.artists(inp))
          songResult = songContainer.desiredSongs.findSongTitle(inp)
          if(artistResult or songResult): #Input was an artist or song
            if(artistResult and songResult): #Choose which
              print(f"{bold(inp)} is both an artist and a song name. Which would you like removed?")
              while(True):
                opt = input(f"Input {underline('1')} for the artist or {underline('2')} for song: ")
                if(opt == '1'):
                  songResult = []
                  break
                elif(opt == '2'):
                  artistResult = []
                  break
              print("Input could not be used. Please try again.")
              input()#Wait for user
            if(artistResult): #Remove artist
              songs += artistResult
              print(f"Found {len(artistResult)} songs from this artist.")
              input()#Wait for user
            else:
              if(len(songResult) > 1):
                print(f"There are {bold(len(songResult))} songs with that title found in the collection. Select which one you would like removed.")
                for i in range(len(songResult)):
                  song = songContainer.desiredSongs[songResult[i]]
                  print(f"{i+1}. {song.title} by {bold(song.artist)} on {bold(song.album)}.")
                while(True):
                  opt = input(f"Select a song: ")
                  try:
                    opt = int(opt) -1
                    assert opt >= 0
                    songResult = [songResult[opt]]
                    break
                  except:
                    print("Input could not be used. Please try again.")
                    input()#Wait for user
                    continue
              song = songContainer.desiredSongs[songResult[0]]
              while(True):
                opt = input(f"Are you sure you want to remove {bold(song.title)} by {bold(song.artist)} on {bold(song.album)}? {bold('(y/n)')} ").lower()
                if(opt == 'n' or opt == 'no'):
                  print("Song will not be removed.")
                  input()#Wait for user
                  break
                elif(opt == 'y' or opt == 'yes'):
                  songs.append(songResult[0])
                  print("Song added to be removed.")
                  input()#Wait for user
                  break
                else:
                  print("Input could not be used. Please try again.")
                  input()#Wait for user 

          #Check if inp is JSON
          elif(inp[-5:] == ".json"):
            fileRes = validatedFile(inp)
            if(type(fileRes) == dict): #Program's JSON
              for uri in fileRes:
                songs.append(uri)
              print(f"Found {len(fileRes)} songs from this file.")
              input()#Wait for user
            elif(type(fileRes) == list): #Spotify's JSON
              for song in fileRes:
                songs.append(song['spotify_track_uri'])
              print(f"Found {len(fileRes)} songs from this file.")
              input()#Wait for user

          #Check if inp is URI
          elif(inp in songContainer.desiredSongs): #URI with spotify:track
            song = songContainer.desiredSongs[inp]
            while(True):
                opt = input(f"Are you sure you want to remove {bold(song.title)} by {bold(song.artist)} on {bold(song.album)}? {bold('(y/n)')} ").lower()
                if(opt == 'n' or opt == 'no'):
                  print("Song will not be removed.")
                  input()#Wait for user
                  break
                elif(opt == 'y' or opt == 'yes'):
                  songs.append(inp)
                  print("Song added to be removed.")
                  input()#Wait for user
                  break
                else:
                  print("Input could not be used. Please try again.")
                  input()#Wait for user 
          elif("spotify:track:"+inp in songContainer.desiredSongs):#URI without spotify:track
            inp = "spotify:track:"+inp
            song = songContainer.desiredSongs[inp]
            while(True):
                opt = input(f"Are you sure you want to remove {bold(song.title)} by {bold(song.artist)} on {bold(song.album)}? {bold('(y/n)')} ").lower()
                if(opt == 'n' or opt == 'no'):
                  print("Song will not be removed.")
                  input()#Wait for user
                  break
                elif(opt == 'y' or opt == 'yes'):
                  songs.append(inp)
                  print("Song added to be removed.")
                  input()#Wait for user
                  break
                else:
                  print("Input could not be used. Please try again.")
                  input()#Wait for user

          else: #inp was a playist (or not found artist/song/file)
            track_results = sp.getPlaylistSongs(inp)
            if(track_results is None):
              print("The input could not be used. This could mean that the artist or song is not in the collection, the file location was not valid, or the playlist given is empty. Remember to enter an item one at a time. Please try again.")
              input()#Wait for user
              continue
            for song in track_results:
              songs.append(song['track']['uri'])
            print(f"Found {len(track_results)} songs from this playlist.")
            input()#Wait for user
      
      if(len(songs) > 0):
        print("Time to remove these songs from the collection!")
        input()
        prevLen = len(songContainer.desiredSongs)
        pBar = ProgressBar(len(songs), 'Removing songs from collection')
        for uri in songs:
          songContainer.forceRemove(uri)
          pBar.updateProgress()
        pBar.finish()
        if(prevLen > len(songContainer.desiredSongs)):
          containerAltered = True
        print(f"Your new total is now {bold(len(songContainer.desiredSongs))} songs!")
        input()#Wait for user
      __terminal__.clear() # type: ignore
      return containerAltered
    elif(inp == 'n' or inp == 'no'):
      return containerAltered
    else:
      print("Input could not be used. Please try again.")
      input()#Wait for user
      __terminal__.clear() # type: ignore
      continue


def resume():
  prev = sAccount.getPrevRes()
  newContainer = MasterSongContainer()
  newContainer.desiredSongs = prev[0]
  if(prev):
    if(prev[1] == "Addto"):
      return addToPlaylist(newContainer)
    elif(prev[1] == "forceAdd"):
      return forceAdd(newContainer)
    elif(prev[1] == "forceRemove"):
      return forceRemove(newContainer)
  else:
    pass #Start main

if __name__ == "__main__":
  resume()

