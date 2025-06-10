from pyscript import fetch
import asyncio
from SpotifyFunctions import SpotifyGateway

if(1-1 == 1): #Always False, used so vscode will give autofill
  from Helpers.SpotifyFunctions import SpotifyGateway



print("HIHIHI")
async def getKeys():
  response = await fetch(
    "https://tkothenbeutel.pyscriptapps.com/divine-poetry/api/proxies/spotify-secrets",
    method= "GET").json
  return await response


def main():
  asyncio.run(getKeys())
  print("GETTING SECRETS")
  user = input("Username: ")
  playlist = input("Playlist: ")
  s = SpotifyGateway(user, playlist)
  s.validateInformation()


main()
if __name__ == "__main__":
  print("In if statement!")
  main()