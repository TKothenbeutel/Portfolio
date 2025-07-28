"""
TODO:
  Test!
  **Future Ideas**
  *ForceRemove can list songs in both data and given playlist
"""
import asyncio
import json
from time import sleep
from datetime import datetime
from Helpers.Formatting import *
from Helpers.SongStruct import MasterSongContainer
from Helpers.ProgressBar import ProgressBar

builtins.print("hihi")
import pyscript
builtins.print(dir(pyscript),'\n\n')
from pyscript import js_modules
builtins.print(dir(js_modules),'\n\n')

try:
  from pyscript.js_modules import sAccount # type: ignore
except Exception as e:
  builtins.print(e)
from pyscript.js_modules import fileReader # type: ignore
from pyscript.js_modules import spotifyJS # type: ignore
from pyscript.js_modules import settings # type: ignore

#from pyscript import when, window

#@when("resize",window)
#def resizeTerminal():
#  columns = settings.getCols()
#  __terminal__.resize(columns, 24) # type: ignore

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
  return welcome()

def saveResults(songContainer: MasterSongContainer):
  plainSongs = songContainer.desiredSongs.export()
  resultToJSON = json.dumps(plainSongs, indent=4)
  name = f'spotify_parsing_{currentTime()}.json'
  fileReader.displayResults(name, resultToJSON)




async def forceAdd(songContainer:MasterSongContainer):
  """Asks user if they would like to force add songs."""
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
    inp = input(f"Before we begin, do you plan on adding songs via a Spotify playlist? {bold('(y/n)')} ").lower()
    while(not inp in ["n","no","y","yes"]):
      print("Input could not be read.")
      inp = input(f"Before we begin, do you plan on adding songs via a Spotify playlist? {bold('(y/n)')} ").lower()
    if(inp == "y" or inp == "yes"):
      input("To do so, you must be signed into your Spotify account through this program. The program will now direct you to Spotify's login page.")
      await sAccount.retreiveToken(f"{json.dumps(songContainer.desiredSongs.export())},forceAdd")

  songs = {}

  while(True):
    inp = ""
    if(token): #Spotify connected
      inp = input(f"Please enter the ID of the playlist or input any JSON files below that contain Spotify song URIs (in the format of the streaming history file). Please note that pasting text will only work by right-clicking on the terminal's cursor. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID. Enter {bold(underline('d')+'one')} when you are finished inputting playlist IDs and files, or enter {bold(underline('c')+'ancel')} if you would not like to add songs: ")
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
        track_results = (await spotifyJS.retreiveTracks(token, inp))
        if(track_results is None):
          print("The input could not be used. This could mean that the playlist given is empty or could not be found. Remember to enter an item one at a time. Please try again.")
          input()#Wait for user
          continue
        track_results = track_results.to_py()
        for song in track_results:
          songs[song['track']['uri']] = {
            'title' : song['track']['name'],
            'artist' : song['track']['artists'][0]['name'] if song['track']['artists'][0]['name'] else song['track']['artists'][0]['type'],
            'album' : song['track']['album']['name']
          }
        print(f"Found {len(track_results)} songs from this playlist.")
        input()#Wait for user
      else:
        print("Input could not be used. Please try again.")
        input()#Wait for user
        continue

    else: #Spotify not connected
      inp = input(f"Please enter JSON files containing Spotify song URIs (in the format of the streaming history file) that you would like to be included below. When finished, press {bold('enter')}, or enter {bold(underline('c')+'ancel')} if you would not like to add songs: ")
      print()#Spacer
      if(inp == ''):
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
        chunks = file[1]
        masterString = ''
        for chunk in chunks:
          masterString += chunk
        fileRes = json.loads(masterString)
        #fileRes = validatedFile(file[1])
        if(type(fileRes) == dict): #Program's JSON
          for uri in fileRes:
            songs[uri] = fileRes[uri]
          input(f"Found {len(fileRes)} songs from {file[0]}.")
        elif(type(fileRes) == list): #Spotify's JSON
          for song in fileRes:
            if(song['spotify_track_uri']):
              songs[song['spotify_track_uri']] = {
                'title' : song['master_metadata_track_name'],
                'artist' : song['master_metadata_album_artist_name'],
                'album' : song['master_metadata_album_album_name']
              }
          input(f"Found {len(fileRes)} songs from {file[0]}.")
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
  return await forceRemove(songContainer)
  

async def forceRemove(songContainer:MasterSongContainer):
  """Asks user if they would like to force remove songs."""
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
    inp = input(f"Before we begin, do you plan on remove songs via a Spotify playlist? {bold('(y/n)')} ").lower()
    while(not inp in ["n","no","y","yes"]):
      print("Input could not be read.")
      inp = input(f"Before we begin, do you plan on remove songs via a Spotify playlist? {bold('(y/n)')} ").lower()
    if(inp == "y" or inp == "yes"):
      input("To do so, you must be signed into your Spotify account through this program. The program will now direct you to Spotify's login page.")
      await sAccount.retreiveToken(f"{json.dumps(songContainer.desiredSongs.export())},forceRemove")

  songs = []

  while(True):
    inp = ""

    if(token): #Spotify connected
      print(f"Please enter any of the following:")
      print(f"   * {bold('Spotify playlist ID')}\n   * {bold('list')} to list all artists still in the container\n   * {bold('list <artist name (case-sensitive)>')} to list all songs in the container by given artist\n   * {bold('Artist name (case-sensitive)')}\n   * {bold('Song title/URI')}")
      inp = input(f"Please enter JSON files containing Spotify song URIs (in the format of the streaming history file) that you would like to be removed below.\nPlease note that pasting text will only work by right-clicking on the terminal's cursor. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID. Enter {bold(underline('d')+'one')} when you are finished inputting items for removal, or enter {bold(underline('c')+'ancel')} if you would not like to remove any songs: ")
      print()#Spacer
      if(inp.lower() == 'help' or inp.lower() == 'h'):
        print(f"To retrieve a playlist's ID, please follow these instructions:\n\t1. Navigate to the web version of Spotify.\n\t2. Open the desired playlist. The URL at this point should look something like {bold('open.spotify.com/playlist/...')}\n\t3. Copy the section of the URL after {bold('/playlist/')}. This key smash of characters is the playlist ID.")
        inp = input("Please enter the desired playlist's ID, artist name, or song title: ").lower()
        print()#Spacer
    else: #Spotify not connected
      print(f"Please enter any of the following:")
      print(f"   * {bold('list')} to list all artists still in the container\n   * {bold('list <artist name (case-sensitive)>')} to list all songs in the container by given artist\n   * {bold('Artist name (case-sensitive)')}\n   * {bold('Song title/URI')}")
      inp = input(f"Please enter JSON files containing Spotify song URIs (in the format of the streaming history file) that you would like to be removed below.\nPlease note that pasting text will only work by right-clicking on the terminal's cursor. Enter {bold(underline('d')+'one')} when you are finished inputting items for removal, or enter {bold(underline('c')+'ancel')} if you would not like to remove any songs: ")
      print()#Spacer

    if(inp.lower() == 'done' or inp.lower() == 'd'):
      break
    elif(inp.lower() == 'cancel' or inp.lower() == 'c'):
      songs = {}
      break

    elif(inp.lower() == "list"):
      if(__terminal__.cols > 70): # type: ignore
        maxCount = 3
      elif(__terminal__.cols > 50): # type: ignore
        maxCount = 2
      else:
        maxCount = 1
      count = 0
      message = ''
      for artist in songContainer.desiredSongs.listArtists():
        bullet = f"    * {artist}"
        while(len(bullet) < (24 if maxCount != 1 else 0)):
          bullet += ' '
        message += bullet
        count += 1
        if(count == maxCount):
          print(message.rstrip())
          message = ''
          count = 0
      input()#Wait for user

    elif(inp[:5].lower() == "list "): #List songs by artist
      songsList = songContainer.desiredSongs.listArtists(inp[5:])
      if(songsList):
        if(__terminal__.cols > 80): # type: ignore
          maxCount = 2
        else:
          maxCount = 1
        count = 0
        message = ''
        for uri in songsList:
          bullet = f"    * {songContainer.desiredSongs.getTitle(uri)} ({songContainer.desiredSongs.getCount(uri)})"
          while(len(bullet) < (40 if maxCount != 1 else 0)):
            bullet += ' '
          message += bullet
          count += 1
          if(count == maxCount):
            print(message.rstrip())
            message = ''
            count = 0
        input()#Wait for user 
      else:
        print("Given artist could not be found in the dataset. Please try again.")
        input()#Wait for user 

    else:#Input of artist/song/playlist
      artistResult = list(songContainer.desiredSongs.artists(inp if inp else " "))
      songResult = songContainer.desiredSongs.findSongTitle(inp if inp else " ")
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
      elif("spotify:track:"+inp in songContainer.desiredSongs or "spotify:episode:"+inp in songContainer.desiredSongs):#URI without spotify:track
        if("spotify:track:"+inp in songContainer.desiredSongs):
          inp = "spotify:track:"+inp
        else:
          inp = "spotify:episode:"+inp
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

      elif(token): #inp was a playist (must have token)
        track_results = (await spotifyJS.retreiveTracks(token, inp))
        if(track_results is None):
          print("The input could not be used. This could mean that the artist or song is not in the collection or the playlist given is empty or could not be found. Remember to enter an item one at a time. Please try again.")
          input()#Wait for user
          continue
        track_results = track_results.to_py()
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
        chunks = file[1]
        masterString = ''
        for chunk in chunks:
          masterString += chunk
        fileRes = json.loads(masterString)
        #fileRes = validatedFile(file[1])
        if(type(fileRes) == dict): #Program's JSON
          for uri in fileRes:
            songs.append(uri)
          input(f"Found {len(fileRes)} songs from {file[0]}.")
        elif(type(fileRes) == list): #Spotify's JSON
          for song in fileRes:
            songs.append(song['spotify_track_uri'])
          input(f"Found {len(fileRes)} songs from {file[0]}.")
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
  #Unblock settings
  for i in ["beginningDate","minCount","minMS","songPreference","minCountOverride","earliestDate","lastDate","playlistAddTimer","songGracePeriod","universalMinCount"]:
    settings.unBlockSetting(i)
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
  #Major variables
  dataContainer = [] #Each item will contain a dictionary of what the JSON file had
  songContainer = MasterSongContainer() #Settings transfer over
  
  __terminal__.clear() # type: ignore
  fileReader.hideResults()
  print("Let's begin!\n")
  input()

  #Gather files
  print("First, let's get every file containing songs from your extended Spotify streaming history.")
  print(f'Please input the JSON files included with your extended Spotify streaming history folder below (the file should be called {bold("Streaming_History_Audio")}...{bold(".json")}). Press {bold('enter')} when all files have been uploaded.')
  while(True):
    input(f'Enter files below and press {bold("enter")} here')
    print(". . .")
    files = fileReader.filesToPy().to_py() #Get files
    if(files):
      fileReader.readOnlySection("parsingFiles") #Gray out
      for file in files:
        try:
          chunks = file[1]
          masterString = ''
          for chunk in chunks:
            masterString += chunk
          fileRes = json.loads(masterString)
          if(fileRes is None):
            Exception()
          dataContainer.append(fileRes)
        except:
          while(True):
            inp = input(f"Could not use {file[0]}. Would you like to restart this process? {bold('(y/n)')} ")
            if(inp.lower() == "n" or inp.lower() == "no"):
              break
            elif(inp.lower() == "y" or inp.lower() == "yes"):
              fileReader.updateFileInputSection("parsingFiles") #Reset Section
              return await run()
            else:
              input("Input could not be read. Please try again.")
      if(dataContainer == []):
        print("The program must have data to parse through. Please try again.")
        input()#Wait for user
        return welcome()
      else:
        break
    else:
      print("You must enter files for the program to parse through. Please try again.")
      input()

  print('Great! Time to add them into containers for easier parsing.')
  print(f"The next step will disable the following settings: {bold('Beginning Date')}, {bold('Minimum Milliseconds')}, {bold('Last Date')}, and {bold('Earliest Date')}.")
  
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
  print(f"The next steps will disable the following settings: {bold('Minimum Count')}, {bold('Song Preference')}, {bold('Minimum Count Override')}, {bold('Song Grace Period')}, and {bold('Universal Minimum Count')}.")
  input()
  songContainer.parse()
  return await combineSongs(songContainer)


async def combineSongs(songContainer: MasterSongContainer):
  token = sAccount.accessToken
  while(settings.getSetting("songPreference") == "ask" and token == ""):
    settings.unBlockSetting("songPreference")
    inp = input(f"You have indicated that you would like to be asked about which duplicate song to keep. This feature requires a Spotify login, which has not yet been given. Would you like to continue and be brought to Spotify's login page? Your data this far will be saved. If you would not like to sign in, then please change the {bold('Song Preference')} setting and respond with no. {bold('(y/n)')} ").lower()
    if(inp == 'y' or inp == 'yes'):
      token = await sAccount.retreiveToken(f"{json.dumps(songContainer.desiredSongs.export())},combineSongs")
  
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
      return end(songContainer)
    else:
      print("Input could not be read. Please try again.")

  token = await sAccount.retreiveToken(f"{json.dumps(songContainer.desiredSongs.export())},Addto")
  user = sAccount.retreiveUser()
  print(f'\nTo add these songs onto a playlist, some information of your {bold("Spotify")} is first needed.')

  playlist_id = input(f"Now, please enter the ID of the playlist you would like the songs added to. Please note that pasting text will only work by right-clicking on the terminal's cursor. Enter {bold(underline('h')+'elp')} for information on how to retrieve a playlist's ID: ")
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
  print("Test has successfully passed. Now it's time to add the songs to the playlist.")
  print(f"The next step will disable the following setting: {bold('Playlist Add Timer')}.")
  input()#Wait for user

  timer = float(settings.getSetting("playlistAddTimer"))
  pBar = ProgressBar(len(songContainer.desiredSongs),"Adding songs to playlist")
  #If timer is >0, run timed adder
  if(timer > 0):
    for uri in songContainer.desiredSongs:
      pBar.updateProgress()
      await spotifyJS.addSongs(token, playlist_id, [uri])
      sleep(timer)
  #Else run batch adder
  else:
    length = len(songContainer.desiredSongs)
    URIs = list(songContainer.desiredSongs)
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
  fileReader.reset()
  return welcome()

async def resume():
  __terminal__.clear() # type: ignore
  fileReader.hideResults()
  print("Welcome back! Let's get your previously saved data.")
  input()

  masterSongs = MasterSongContainer()

  print(f"First, please upload your result file gained from previously using this program below. Ensure this file has not been altered, otherwise, the program may not be able to read the file.")
  while(True):
    input(f"Press {bold('enter')} here when all files have been uploaded")
    print(". . .")
    files = fileReader.filesToPy().to_py() #Get files
    if(files):
      try:
        fileReader.readOnlySection("parsingFiles") #Gray out
        chunks = files[0][1]
        masterString = ''
        for chunk in chunks:
          masterString += chunk
        fileRes = json.loads(masterString)
        #fileRes = validatedFile(file[1])
        if(fileRes is None):
          Exception()
        addResult = masterSongs.desiredSongs.addFromFile(fileRes)
        if(not addResult):
          print("The given file could be read, but it could not be used in this program. Please ensure you are uploading an unedited result file from this program previously so that you may continue to next step.")
          masterSongs = MasterSongContainer()
          continue
        break
      except:
        print(f"{files[0][0]} could not be used. Please try again.")
        fileReader.updateFileInputSection("parsingFiles") #Refresh section
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
    prev = prev.rsplit(',',1)
    newContainer = MasterSongContainer()
    newContainer.desiredSongs.addFromFile(json.loads(prev[0]))
    __terminal__.clear() # type: ignore
    #Gray out previous settings
    for i in ["beginningDate","minCount","minMS","songPreference","minCountOverride","earliestDate","lastDate","songGracePeriod","universalMinCount"]:
        settings.getSetting(i)
    #Prevent file upload into file to parsingFiles
    fileReader.readOnlySection("parsingFiles")
    #Return to section
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
    return welcome()

if __name__ == "__main__":
  #resizeTerminal()
  continueSession()