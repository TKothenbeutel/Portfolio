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
import json
from time import sleep
from datetime import datetime
from Helpers.Formatting import *
from Helpers.DataParse import validatedFile, dictToJSON
from Helpers.SongStruct import MasterSongContainer
from Helpers.ProgressBar import ProgressBar

from pyscript.js_modules import sAccount # type: ignore
from pyscript.js_modules import fileReader # type: ignore
from pyscript.js_modules import spotifyJS # type: ignore
from pyscript.js_modules import settings # type: ignore


def currentTime():
  return f'{datetime.today().date()}_{str(datetime.today().time()).replace(":","-")[:8]}'

def runAsync(task):
  loop = asyncio.get_event_loop()
  res = loop.run_until_complete(task)
  return res

def about():
  __terminal__.clear() # type: ignore
  print(f'Made by {bold("Taylor Kothenbeutel")}')
  input()

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

async def forceAdd(songContainer:MasterSongContainer):
  """Asks user if they would like to force add songs."""
  __terminal__.clear() # type: ignore

  inp = input(f"I'm sure you got some great songs snagged already, but would you like any songs forced in the collection, regardless of the song's uniqueness? {bold('(y/n)')} ").lower()
  if(not(inp == 'y' or inp == 'yes')):
    if(inp == 'n' or inp == 'no'):
      return await forceRemove(songContainer)
    else:
      print("Input could not be used. Please try again." )
      input()
      return await forceAdd(songContainer)

  fileReader.updateFileInputSection("forceAddFiles") #Open section
  print("Sounds good! Please note that the timestamp added to these songs will be today's date and current time. If you save your song results, the songs added via this method will have a count of 0.")
  print()#Spacer

  token = sAccount.accessToken
  if(token == ""):
    inp = input(f"Before we begin, do you plan on adding songs via a Spotify playlist? {bold('y/n')} ").lower()
    while(not inp in ["n","no","y","yes"]):
      print("Input could not be read.")
      inp = input(f"Before we begin, do you plan on adding songs via a Spotify playlist? {bold('y/n')} ").lower()
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
          inp = input(f"Could not use {file[0]}. Would you like to restart the force add process? {bold('y/n')} ")
          if(inp.lower() == "n" or inp.lower() == "no"):
            break
          elif(inp.lower() == "y" or inp.lower() == "yes"):
            return await forceAdd(songContainer)
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
        songContainer.forceAdd(uri, songs[uri]['title'], songs[uri]['artist'], songs[uri]['album'])
        pBar.updateProgress()
    pBar.finish()
    print(f"Your new total is now {bold(len(songContainer.desiredSongs))} songs!")
    input()#Wait for user
    __terminal__.clear() # type: ignore
  return await forceRemove(songContainer)
  



async def forceRemove(songContainer:MasterSongContainer):
  """Asks user if they would like to force remove songs."""
  __terminal__.clear() # type: ignore

  inp = input(f"Would you like to force remove any songs from this collection? {bold('(y/n)')} ").lower()
  if(not(inp == 'y' or inp == 'yes')):
    if(inp == 'n' or inp == 'no'):
      return await addToPlaylist(songContainer)
    else:
      print("Input could not be used. Please try again." )
      input()
      return await forceRemove(songContainer)

  fileReader.updateFileInputSection("forceRemoveFiles") #Open section
  print("Sounds good!")
  print()#Spacer

  token = sAccount.accessToken
  if(token == ""):
    inp = input(f"Before we begin, do you plan on remove songs via a Spotify playlist? {bold('y/n')} ").lower()
    while(not inp in ["n","no","y","yes"]):
      print("Input could not be read.")
      inp = input(f"Before we begin, do you plan on remove songs via a Spotify playlist? {bold('y/n')} ").lower()
    if(inp == "y" or inp == "yes"):
      input("To do so, you must be signed into your Spotify account through this program. The program will now direct you to Spotify's login page.")
      await sAccount.retreiveToken((songContainer.desiredSongs,"forceAdd"))

  songs = []

  while(True):
    inp = ""

    if(token): #Spotify connected
      print(f"Please enter any of the following:")
      print(f"   * Spotify playlist ID\n   * {bold('list <artist name (case-sensitive)>')} to list all songs in the container by given artist\n   * Artist name (case-sensitive)\n   * Song title/URI")
      inp = input(f"Please enter JSON files containing Spotify song URIs (in the format of the streaming history file) that you would like to be removed below. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID. Enter {bold(underline('d')+'one')} when you are finished inputting items for removal, or enter {bold(underline('c')+'ancel')} if you would not like to remove any songs: ")
      print()#Spacer
      if(inp.lower() == 'help' or inp.lower() == 'h'):
        print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
        inp = input("Please enter the desired playlist's ID, artist name, or song title: ").lower()
        print()#Spacer
    else: #Spotify not connected
      print(f"Please enter any of the following:")
      print(f"   * {bold('list <artist name (case-sensitive)>')} to list all songs in the container by given artist\n   * Artist name (case-sensitive)\n   * Song title/URI")
      inp = input(f"Please enter JSON files containing Spotify song URIs (in the format of the streaming history file) that you would like to be removed below. Enter {bold(underline('d')+'one')} when you are finished inputting items for removal, or enter {bold(underline('c')+'ancel')} if you would not like to remove any songs: ")
      print()#Spacer

    if(inp.lower() == 'done' or inp.lower() == 'd'):
      break
    elif(inp.lower() == 'cancel' or inp.lower() == 'c'):
      songs = {}
      break

    elif(inp[:5].lower() == "list "): #List songs by artist
      pass #TODO

    else:#Input of artist/song/playlist
      artistResult = list(songContainer.desiredSongs.artists(inp))
      songResult = songContainer.desiredSongs.findSongTitle(inp)
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

      elif(songResult): #Remove song
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

      elif(token): #inp was a playist (must have token)
        track_results = (await spotifyJS.retreiveTracks(token, inp)).to_py()
        if(track_results is None):
          print("The input could not be used. This could mean that the artist or song is not in the collection or the playlist given is empty or could not be found. Remember to enter an item one at a time. Please try again.")
          input()#Wait for user
          continue
        for song in track_results:
          songs.append(song['track']['uri'])
        print(f"Found {len(track_results)} songs from this playlist.")
        input()#Wait for user

      else: #Doesn't match any criteria
        print("The input could not be used. This could mean that the artist or song is not in the collection. Remember to enter an item one at a time. Please try again.")
        input()#Wait for user
        continue

  #Check for any inputted files
  fileReader.readOnlySection("forceRemoveFiles") #Gray out
  files = fileReader.filesToPy().to_py() #Get files
  if(files):
    for file in files:
      try:
        fileRes = validatedFile(file[1])
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
      except:
        while(True):
          inp = input(f"Could not use {file[0]}. Would you like to restart the force remove process? {bold('y/n')} ")
          if(inp.lower() == "n" or inp.lower() == "no"):
            break
          elif(inp.lower() == "y" or inp.lower() == "yes"):
            return await forceRemove(songContainer)
          else:
            print("Input could not be read. Please try again.")
  
  if(len(songs) > 0):
    print("Time to remove these songs from the collection!")
    input()
    pBar = ProgressBar(len(songs), 'Removing songs from collection')
    for uri in songs:
      songContainer.forceRemove(uri)
      pBar.updateProgress()
    pBar.finish()
    print(f"Your new total is now {bold(len(songContainer.desiredSongs))} songs!")
    input()#Wait for user
  return await addToPlaylist(songContainer)

def welcome():
  """Prints messages that appear at the start of the program."""
  __terminal__.clear() # type: ignore
  print(f'Welcome to the {bold("Spotify Unique Song Parser")}!')
  print(f'{bold(underline("S")+"tart")}: Start the process to parse through your data')
  print(f'{bold(underline("R")+"esume")}: Use previous program results and skip the parsing')
  print(f'{bold(underline("A")+"bout")}: Learn more about this program')
  inp = input('\n\n').lower()
  if(inp == 'start' or inp == 's'):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(loop.create_task(run()))
    loop.close()
  elif(inp == 'resume' or inp == 'r'):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(loop.create_task(resume()))
    loop.close()
  elif(inp == 'about' or inp == 'a'):
    about()
  else:
    print("Input could not be used. Please try again.")
    input()
    return welcome()
  
async def run():
  fileReader.updateFileInputSection("parsingFiles") #Open section
  #Major variables
  dataContainer = [] #Each item will contain a dictionary of what the JSON file had
  songContainer = MasterSongContainer() #Settings transfer over
  
  __terminal__.clear() # type: ignore
  print("Let's begin!\n")
  input()

  #Gather files
  print("First, let's get every file containing songs from your extended Spotify streaming history.")
  print(f'Please input the JSON files included with your extended Spotify streaming history folder below (the file should be called {bold("Streaming_History_Audio")}...{bold(".json")}). Input {bold(underline("d")+"one")} here when all files have been uploaded.')
  while(True):
    inp = input(f'Enter files below and enter {bold(underline("d")+"one")} here: ')
    if(inp.lower() == 'done' or inp.lower() == 'd'):
      files = fileReader.filesToPy().to_py() #Get files
      if(files):
        fileReader.readOnlySection("parsingFiles") #Gray out
        for file in files:
          masterString = ''
          for chunk in file[1]:
            masterString += chunk
          fileRes = json.loads(masterString)
          #fileRes = validatedFile(file[1])
          if(fileRes is None):
            inp = input(f"Could not use {file[0]}. Would you like to restart this process? {bold('(y/n)')} ")
            if(inp.lower() == "n" or inp.lower() == "no"):
              continue
            elif(inp.lower() == "y" or inp.lower() == "yes"):
              return run()
            else:
              print("Input could not be read. Please try again.")
          else:
            dataContainer.append(fileRes)
        if(dataContainer == []):
          print("The program must have data to parse through. Please try again.")
          input()#Wait for user
          return welcome()
        else:
          break
      else:
        print("You must enter files for the program to parse through. Please try again.")
        input()
    else:
      print("Input could not be read. Please try again.")

  print()#Spacing

  print('Great! Time to add them into containers for easier parsing.')
  
  input()#Wait for user

  #Get total number of songs
  numberSongs = 0
  for i in dataContainer:
    numberSongs += len(i)

  #Add songs to collection
  pBar = ProgressBar(numberSongs, 'Adding songs to containers')
  for chunk in dataContainer:
    for entry in chunk:
      pBar.updateProgress()
      songContainer.addSong(entry)
  pBar.finish()

  #Adding to container results
  print(f"After adding all the songs to their respective containers, {bold(len(songContainer.desiredSongs))} of the {bold(len(songContainer.desiredSongs)+len(songContainer.previousSongs))} songs are potentially unique songs listened to in the given range. Let's shrink that number!")

  input()#Wait for user

  #Parse
  print("Now that all songs have been accounted for, let's get parsing!")
  input()
  songContainer.parse()
  return await combineSongs(songContainer)


async def combineSongs(songContainer: MasterSongContainer):
  token = sAccount.accessToken
  while(settings.getSetting("songPreference") == "ask" and token == ""):
    inp = input(f"You have indicated that you would like to be asked about which duplicate song to keep. This feature requires a Spotify login, which has not yet been given. Would you like to continue and be brought to Spotify's login page? Your data this far will be saved. If you would not like to sign in, then please change the {bold('Song Preference')} setting and respond with no. (y/n)").lower()
    if(inp == 'y' or inp == 'yes'):
      token = await sAccount.retreiveToken((songContainer.desiredSongs,"combineSongs"))
  
  await songContainer.combineSongs(token)

  print()#Spacing

  #Announce results
  print(f"Parsing is now complete! In all, the program found {bold(len(songContainer.desiredSongs))} unique songs. That's a lot of songs (probably)!")

  input()#Wait for user

  #Force add or remove any songs
  return await forceAdd(songContainer)

async def addToPlaylist(songContainer:MasterSongContainer):
  #Sort collection
  songContainer.sort()

  #Save for later or add to playlist
  while(True):
    inp = input(f"Would you like to add your results into a Spotify playlist? {bold('(y/n)')} ").lower()
    if(inp == 'y' or inp == 'yes'):
      break
    elif(inp == 'n' or inp == 'no'):
      return end()
    else:
      print("Input could not be read. Please try again.")

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

  timer = float(settings.getSetting("playlistAddTimer"))
  pBar = ProgressBar(len(songContainer.desiredSong),"Adding songs to playlist")
  #If timer is >0, run timed adder
  if(timer > 0):
    for uri in songContainer.desiredSong:
      pBar.updateProgress()
      await spotifyJS.addSongs(token, playlist_id, [uri])
      sleep(timer)
  #Else run batch adder
  else:
    length = len(songContainer.desiredSong)
    URIs = list(songContainer.desiredSong)
    begIndex = 0
    #Add songs in bactches of 100
    while(length - begIndex >= 100):
      pBar.updateProgress(100)
      await spotifyJS.addSongs(token, playlist_id, URIs[begIndex:begIndex+100])
      begIndex += 100
    #Add remaining songs
    pBar.updateProgress(length-begIndex)
    await spotifyJS.addSongs(token, playlist_id, URIs[begIndex:])
  pBar.finish()
  print('All songs successfully added to the playlist.')
  input()
  return end(songContainer)

def end(songContainer: MasterSongContainer):
  saveResults(songContainer)
  print("You may download your results below.")

  #After saving/adding/bothing
  print(f'This program is now finished. {bold("Thank you for using it!")}')
  input()
  return welcome()

async def resume():
  fileReader.updateFileInputSection("forceRemoveFiles") #Open section
  __terminal__.clear() # type: ignore
  print("Welcome back! Let's get your previously saved data.")
  input()

  masterSongs = MasterSongContainer()

  print(f"First, please upload your result file gained from previously using this program below. Ensure this file has not been altered, otherwise, the program may not be able to read the file.")
  while(True):
    inp = input(f"Enter {bold(underline('d')+'one')} here when all files have been uploaded: ")
    if(inp.lower() not in ["d","done"]):
      print("Input could not be read. Please try again.")
      continue
    files = fileReader.filesToPy().to_py() #Get files
    if(files):
      fileReader.readOnlySection("parsingFiles") #Gray out
      file = files[0]
      masterString = ''
      for chunk in files[1]:
        masterString += chunk
      fileRes = json.loads(masterString)
      #fileRes = validatedFile(file[1])
      if(fileRes is None):
          print("File could not be used. Please try again.")
          fileReader.updateFileInputSection("parsingFiles") #Refresh section
      else:
        addResult = masterSongs.desiredSongs.addFromFile(fileRes)
        if(not addResult):
          print("The given file could be read, but it could not be used in this program. Please ensure you are uploading an unedited result file from this program previously so that you may continue to next step.")
          masterSongs = MasterSongContainer()
          continue
        break
    else:
      print("You must enter a file from your previous result to continue.")
      fileReader.updateFileInputSection("parsingFiles") #Refresh section
  
  #Songs added
  print(f"All {len(masterSongs.desiredSongs)} songs have been imported. Let's move on.")
  input()#Wait for user

  #Force add/remove
  return await forceAdd(masterSongs)

def continueSession():
  prev = sAccount.getPrevRes()
  if(prev):
    newContainer = MasterSongContainer()
    newContainer.desiredSongs = prev[0]
    if(prev[1] == "Addto"):
      loop = asyncio.new_event_loop()
      loop.run_until_complete(loop.create_task(addToPlaylist(newContainer)))
      loop.close()
    elif(prev[1] == "forceAdd"):
      loop = asyncio.new_event_loop()
      loop.run_until_complete(loop.create_task(forceAdd(newContainer)))
      loop.close()
    elif(prev[1] == "forceRemove"):
      loop = asyncio.new_event_loop()
      loop.run_until_complete(loop.create_task(forceRemove(newContainer)))
      loop.close()
    elif(prev[1] == "combineSongs"):
      loop = asyncio.new_event_loop()
      loop.run_until_complete(loop.create_task(combineSongs(newContainer)))
      loop.close()
  else:
    welcome()



if __name__ == "__main__":
  continueSession()

