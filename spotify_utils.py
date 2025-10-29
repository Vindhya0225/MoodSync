import requests
from spotify_auth import get_access_token  # Use refreshed token

# Function to get songs based on mood & age
def get_playlist(mood, age):
    spotify_token = get_access_token()  # Use the refreshed token
    headers = {"Authorization": f"Bearer {spotify_token}"}

    # Define age group playlists based on mood (customized for your project)
    age_mood_playlists = {
        'happy': {
            (14, 30): "https://open.spotify.com/embed/playlist/37i9dQZF1DWTwbZHrJRIgD?utm_source=generator",
            (31, 55): "https://open.spotify.com/embed/playlist/0Gd0yQzB6wttuaLlawHlYI?utm_source=generator",
            (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
        },
        'sad': {
            (14, 30): "https://open.spotify.com/embed/playlist/189Sow1xr7R94oSKs4kISc?utm_source=generator",
            (31, 55): "https://open.spotify.com/embed/playlist/2kdY9Y1eKWLSv51F8gTtel?utm_source=generator"
        },
        'relaxed': {
            (14, 30): "https://open.spotify.com/embed/playlist/02uXGKglrYZD67gcyxkvTd?utm_source=generator",
            (31, 55): "https://open.spotify.com/embed/playlist/07tybyyZQJ0Ps8PdOaCz4m?utm_source=generator"
        },
        'excited': {  # Ensuring the mood name is 'excited'
            (14, 30): "https://open.spotify.com/embed/playlist/3mSm688yR6UeaAJNf93Ydr?utm_source=generator",
            (31, 55): "https://open.spotify.com/embed/playlist/37i9dQZF1DWWQ4RVrwACVr?utm_source=generator"
        }
    }

    # Find the correct playlist based on age and mood
    selected_playlist = None
    for age_range, moods in age_mood_playlists.items():
        if age_range[0] <= age <= age_range[1]:
            if age_range == (56, 100):  # For age 56 and above, use the same playlist regardless of mood
                selected_playlist = moods.get("GoodOldTimes")
            else:
                selected_playlist = moods.get(mood.lower())
            break

    if not selected_playlist:
        return "No playlist found for this mood and age group."

    return selected_playlist  # Return the playlist URI
