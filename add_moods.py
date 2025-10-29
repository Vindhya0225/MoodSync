from app import app, db
from models import Mood

moods_data = [
    {"age_group": "14-30", "mood": "happy", "playlist": "https://open.spotify.com/playlist/37i9dQZF1DWTwbZHrJRIgD?si=ua8ZxG7MRh-47LYaBErsWQ"},
    {"age_group": "14-30", "mood": "sad", "playlist": "https://open.spotify.com/playlist/189Sow1xr7R94oSKs4kISc?si=vayPn86zQ1iaoC47Sue8nQ"},
    {"age_group": "14-30", "mood": "relaxed", "playlist": "https://open.spotify.com/playlist/02uXGKglrYZD67gcyxkvTd?si=y8YFazOYTlGx5EvqlGWsow"},
    {"age_group": "14-30", "mood": "excited", "playlist": "https://open.spotify.com/playlist/3mSm688yR6UeaAJNf93Ydr?si=XzF9NoToR0qNnWikoPEYSQ"},
    {"age_group": "31-55", "mood": "happy", "playlist": "https://open.spotify.com/playlist/0Gd0yQzB6wttuaLlawHlYI?si=L9vbFAEfQOmWro9TPMZhfg"},
    {"age_group": "31-55", "mood": "sad", "playlist": "https://open.spotify.com/playlist/2kdY9Y1eKWLSv51F8gTtel?si=mclpC-y9QamhY1FFfHG6Jg"},
    {"age_group": "31-55", "mood": "relaxed", "playlist": "https://open.spotify.com/playlist/07tybyyZQJ0Ps8PdOaCz4m?si=WQ2Lxx0SQFaqj8Cyg3DpJA"},
    {"age_group": "31-55", "mood": "excited", "playlist": "https://open.spotify.com/playlist/37i9dQZF1DWWQ4RVrwACVr?si=kZ3rKqSBQuqy00J2GODzcA"},
    {"age_group": "56+", "mood": "happy", "playlist": "https://open.spotify.com/playlist/1g0ObStnohqvNXeDhyXVE7?si=_6HHGECvQ7q0pi_tpjur1Q"},
    {"age_group": "56+", "mood": "sad", "playlist": "https://open.spotify.com/playlist/1g0ObStnohqvNXeDhyXVE7?si=_6HHGECvQ7q0pi_tpjur1Q"},
    {"age_group": "56+", "mood": "relaxed", "playlist": "https://open.spotify.com/playlist/1g0ObStnohqvNXeDhyXVE7?si=_6HHGECvQ7q0pi_tpjur1Q"},
    {"age_group": "56+", "mood": "excited", "playlist": "https://open.spotify.com/playlist/1g0ObStnohqvNXeDhyXVE7?si=_6HHGECvQ7q0pi_tpjur1Q"}
]

with app.app_context():  # Ensure the app context is available
    for mood in moods_data:
        new_mood = Mood(age_group=mood["age_group"], mood=mood["mood"], playlist=mood["playlist"])
        db.session.add(new_mood)

    db.session.commit()

print("Moods added successfully!")
