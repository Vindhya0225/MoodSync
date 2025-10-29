# spotify_auth.py

import requests
import base64

CLIENT_ID = "94c6dc0aceab4636ba7106aaad00a863"
CLIENT_SECRET = "f900f6261eac4bb4a7215fed828626ab"

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")
