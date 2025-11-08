import requests
import base64

CLIENT_ID = "# Replace with your actual Client ID"  # Get both from spotify developer dashboard by creatong a new project
CLIENT_SECRET = "Replace with your actual Client Secret"  

def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

# Get the token
spotify_token = get_spotify_token()
print("Spotify Token:", spotify_token)

