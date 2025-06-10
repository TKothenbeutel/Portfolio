from pyscript import fetch

response = await fetch(
    "https://tkothenbeutel.pyscriptapps.com/divine-poetry/api/proxies/spotify-secrets",
    method= "GET"
).json()

print(response)