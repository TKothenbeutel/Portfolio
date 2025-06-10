from pyscript import fetch

print("HIHIHI")

response = await fetch(
  "https://tkothenbeutel.pyscriptapps.com/divine-poetry/api/proxies/spotify-secrets",
  method= "GET")
if response.ok:
  data = await response.json()
  for i in data:
    print(i['id'])
  
else:
  print(response.status)

def main():
  print("GETTING SECRETS")
  #getSecrets()

main()
if __name__ == "__main__":
  print("In if statement!")
  main()