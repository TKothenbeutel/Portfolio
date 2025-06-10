from pyscript import fetch

print("HIHIHI")

response = await fetch(
  "https://tkothenbeutel.pyscriptapps.com/divine-poetry/api/proxies/spotify-secrets",
  method= "GET").json

for i in response:
  print(i['id'])

def main():
  print("GETTING SECRETS")
  #getSecrets()

main()
if __name__ == "__main__":
  print("In if statement!")
  main()