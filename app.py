from flask import Flask, request, jsonify, render_template, redirect, url_for, session,  make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies

from flask_migrate import Migrate 
from models import db, User, Mood, UserProfile, ListeningReport, UserPlaylist, ModifyPlaylist # ✅ Use imported db from models.py
from routes import routes
from flask_cors import CORS
from spotify_utils import get_playlist
import requests 
import google.generativeai as genai
#from flask_login import login_required, current_user
from datetime import datetime, timedelta
import os
import json
from werkzeug.security import check_password_hash  # Use if passwords are hashed
from flask_session import Session


app = Flask(__name__)
CORS(app) 

genai.configure(api_key="AIzaSyBqY3p2gBNGUaHmiFjBs0NL-zzpxbT9TGc")
# Load Gemini Model
geminiModel = genai.GenerativeModel("gemini-1.5-pro-latest")
chat = geminiModel.start_chat(history=[])

# Database Configuration (Change this to match your PostgreSQL setup)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/moodsync_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
#app.config['SECRET_KEY'] = '2832a84926bd5f0cc001914f59767f0362f6226a3fdc6f43e137d95bbc7c2976'
app.config['SESSION_TYPE'] = 'filesystem'  # Or 'redis' for production
Session(app)

db.init_app(app)  # ✅ Initialize db properly
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

app.register_blueprint(routes)

CLIENT_ID = "94c6dc0aceab4636ba7106aaad00a863"
CLIENT_SECRET = "f900f6261eac4bb4a7215fed828626ab"

app.secret_key = "2832a84926bd5f0cc001914f59767f0362f6226a3fdc6f43e137d95bbc7c2976"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/register-page')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/mood-selection')
def mood_selection():
    return render_template('mood_selection.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

# User Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if not user or user.password != data.get('password'):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    session['user_id'] = user.id  # Store in session for navigation
    return jsonify(access_token=access_token), 200



@app.route('/mood', methods=['POST'])
def get_playlist():
    data = request.json
    mood = data.get('mood')
    age = data.get('age')
    

    if not mood or not age:
        return jsonify({"message": "Mood and age are required"}), 400

    try:
        age = int(age)
    except ValueError:
        return jsonify({"message": "Age must be a valid number"}), 400

    # Map age to the correct age group (stored as a character field in DB)
    if 14 <= age <= 30:
        age_group = "14-30"
    elif 31 <= age <= 55:
        age_group = "31-55"
    elif age >= 56:
        age_group = "56+"
    else:
        return jsonify({"message": "Invalid age"}), 400

    # Query the Mood table using both mood and age_group
    mood_entry = Mood.query.filter_by(mood=mood, age_group=age_group).first()


    if mood_entry:
        return jsonify({"playlist": mood_entry.playlist})
    else:
        return jsonify({"message": "No playlist found for the selected mood and age group"}), 404


# Spotify Playlist Route
@app.route("/api/get_playlist", methods=["GET"])
def get_playlist_api():
    # Get the mood and age parameters from the URL query string
    mood = request.args.get("mood")
    age = request.args.get("age")

    # Log the incoming values to check if they are received properly
    print(f"Received mood: {mood}, age: {age}")

    # Check if the 'mood' and 'age' parameters are correctly passed
    if not mood or not age:
        return jsonify({"message": "Both mood and age are required"}), 400

    try:
        age = int(age)  # Convert age to integer
    except ValueError:
        return jsonify({"message": "Age must be a valid number"}), 400

    # Define the embed URLs for each combination of mood and age group
    playlists = {
        'happy': {
            (14, 30): "https://open.spotify.com/embed/playlist/37i9dQZF1DWTwbZHrJRIgD?utm_source=generator",
            (31, 55): "https://open.spotify.com/embed/playlist/0Gd0yQzB6wttuaLlawHlYI?utm_source=generator",
            (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
        },
        'sad': {
            (14, 30): "https://open.spotify.com/embed/playlist/189Sow1xr7R94oSKs4kISc?utm_source=generator",
            (31, 55): "https://open.spotify.com/embed/playlist/2kdY9Y1eKWLSv51F8gTtel?utm_source=generator",
            (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
        },
        'relaxed': {
            (14, 30): "https://open.spotify.com/embed/playlist/02uXGKglrYZD67gcyxkvTd?utm_source=generator",
            (31, 55): "https://open.spotify.com/embed/playlist/07tybyyZQJ0Ps8PdOaCz4m?utm_source=generator",
            (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
        },
        'excited': {  # Ensuring the mood name is 'excited'
            (14, 30): "https://open.spotify.com/embed/playlist/3mSm688yR6UeaAJNf93Ydr?utm_source=generator",
            (31, 55): "https://open.spotify.com/embed/playlist/37i9dQZF1DWWQ4RVrwACVr?utm_source=generator",
            (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
        }
    }

    # Get the appropriate playlist URL based on mood and age
    if mood in playlists:
        for (min_age, max_age), playlist_url in playlists[mood].items():
            if min_age <= age <= max_age:
                print(f"Returning playlist: {playlist_url}")
                return jsonify({"playlist": playlist_url})
            
    
    print("No playlist found for the given mood and age range.")
    return jsonify({"message": "No playlist found for this mood and age range."}), 404

@app.route("/refresh_token", methods=["GET"])
def refresh_token():
    refresh_token = request.args.get("refresh_token")
    token_url = "https://accounts.spotify.com/api/token"

    response = requests.post(token_url, data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })

    return jsonify(response.json())  # Returns new access token


    
# Store conversation state
chat_state = {
    "history": [],
    "confirm_mood": False,
    "asking_age": False,
    "detected_mood": None
}

# Define playlists based on mood and age
playlists_chat = {
    'happy': {
        (14, 30): "https://open.spotify.com/embed/playlist/37i9dQZF1DWTwbZHrJRIgD?utm_source=generator",
        (31, 55): "https://open.spotify.com/embed/playlist/0Gd0yQzB6wttuaLlawHlYI?utm_source=generator",
        (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
    },
    'sad': {
        (14, 30): "https://open.spotify.com/embed/playlist/189Sow1xr7R94oSKs4kISc?utm_source=generator",
        (31, 55): "https://open.spotify.com/embed/playlist/2kdY9Y1eKWLSv51F8gTtel?utm_source=generator",
        (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
    },
    'relaxed': {
        (14, 30): "https://open.spotify.com/embed/playlist/02uXGKglrYZD67gcyxkvTd?utm_source=generator",
        (31, 55): "https://open.spotify.com/embed/playlist/07tybyyZQJ0Ps8PdOaCz4m?utm_source=generator",
        (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
    },
    'excited': {
        (14, 30): "https://open.spotify.com/embed/playlist/3mSm688yR6UeaAJNf93Ydr?utm_source=generator",
        (31, 55): "https://open.spotify.com/embed/playlist/37i9dQZF1DWWQ4RVrwACVr?utm_source=generator",
        (56, float('inf')): "https://open.spotify.com/embed/playlist/1g0ObStnohqvNXeDhyXVE7?utm_source=generator"
    }
}

# Mood keywords
mood_keywords = {
    "happy": ["good", "great", "awesome", "fantastic", "amazing", "happy"],
    "sad": ["bad", "upset", "down", "depressed", "sad"],
    "relaxed": ["chill", "relaxed", "calm", "peaceful"],
    "excited": ["excited", "hyped", "energetic", "pumped"]
}

# Detect mood based on message history
def detect_mood(messages):
    text = " ".join(messages).lower()
    for mood, keywords in mood_keywords.items():
        if any(word in text for word in keywords):
            return mood
    return None

# Determine age group for playlist selection
def get_playlist(mood, age):
    for age_range, url in playlists_chat[mood].items():
        if age_range[0] <= age <= age_range[1]:
            return url
    return None

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    chat_state["history"].append(user_message)

    # Detect mood after 3 messages
    if len(chat_state["history"]) == 3 and chat_state["detected_mood"] is None:
        chat_state["detected_mood"] = detect_mood(chat_state["history"])
        chat_state["confirm_mood"] = True
        return jsonify({
            "response": f"I sense that you're feeling {chat_state['detected_mood']}. Would you like to listen to some songs to match your mood? 🎵 (yes/no)",
            "next_step": "confirm_mood",
            "mood": chat_state["detected_mood"]
        })

    # Handle mood confirmation
    if chat_state["confirm_mood"]:
        if user_message.lower() == "yes":
            chat_state["confirm_mood"] = False
            chat_state["asking_age"] = True
            return jsonify({
                "response": "Great! Could you please tell me your age?",
                "next_step": "ask_age"
            })
        else:
            chat_state["confirm_mood"] = False
            chat_state["detected_mood"] = None  # Reset mood detection
            return jsonify({"response": "No problem! Let’s continue our conversation."})

    # Handle age input and suggest a playlist
    if chat_state["asking_age"]:
        try:
            user_age = int(user_message)
            chat_state["asking_age"] = False

            if chat_state["detected_mood"] is None:
                return jsonify({"response": "Oops! I lost track of your mood. Let's try again!"})

            mood = chat_state["detected_mood"]
            playlist_url = get_playlist(mood, user_age)

            return jsonify({
                "response": f"Here's a playlist for your {mood} mood:",
                "playlist": playlist_url
            }) if playlist_url else jsonify({"response": "I couldn't find a playlist for your mood and age."})

        except ValueError:
            return jsonify({"response": "Oops! That doesn't seem like a valid age. Please enter a number."})

    # Default chatbot response
    try:
        response = chat.send_message(str(user_message), stream=True)
        ai_response = "".join(chunk.text for chunk in response)
        return jsonify({"response": ai_response.strip()})
    except Exception as e:
        print("Error in AI response:", e)  # Debugging info
        return jsonify({"error": str(e)}), 500
    
@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    reports = ListeningReport.query.filter_by(user_id=user_id).all()
    playlist = UserPlaylist.query.filter_by(user_id=user_id).all()

    print("Playlist for user:", user_id)
    for song in playlist:
        print(song.song_url)  # Debugging output

    return render_template('profile.html', profile=user_profile, reports=reports, playlist=playlist)

@app.route('/create_profile', methods=['POST'])
def create_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    name = request.form.get('name')
    age = request.form.get('age')
    bio = request.form.get('bio')

    new_profile = UserProfile(user_id=user_id, name=name, age=age, bio=bio)
    db.session.add(new_profile)
    db.session.commit()
    
    return redirect(url_for('profile'))

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    profile = UserProfile.query.filter_by(user_id=user_id).first()

    if profile:
        profile.name = request.form.get('name')
        profile.age = request.form.get('age')
        profile.bio = request.form.get('bio')
        db.session.commit()

    return redirect(url_for('profile'))

@app.route('/add_song', methods=['POST'])
def add_song():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    song_url = request.form.get('song_url')

    # Ensure the URL is an embedded Spotify track link
    if not song_url.startswith("https://open.spotify.com/embed/track/"):
        song_url = song_url.replace("https://open.spotify.com/track/", "https://open.spotify.com/embed/track/")  

    # Check if the song already exists in the user's playlist
    existing_song = UserPlaylist.query.filter_by(user_id=user_id, song_url=song_url).first()
    if existing_song:
        print("Song already exists in playlist!")  # Debug log
        return redirect(url_for('profile'))

    # Add the song if it's not a duplicate
    new_song = UserPlaylist(user_id=user_id, song_url=song_url)
    print(f"Adding song: {new_song.user_id}, {new_song.song_url}")  # Debugging output
    db.session.add(new_song)
    db.session.commit()
    print("Song added to database!")  # Debug log

    return redirect(url_for('profile'))  # Redirect to profile after saving

# Sample list of Spotify embed URLs (can be stored in a database instead)
spotify_iframes = [
    "https://open.spotify.com/embed/track/3hPaDcKCf39Jzp066kY5Xy",
    "https://open.spotify.com/embed/track/5orNEFkFG4RP24goF02AuD",
    "https://open.spotify.com/embed/track/6FahmzZYKH0zb2f9hrVsvw"
]

@app.route('/')
def spot():
    return render_template("spot_UP.html", spotify_iframes=spotify_iframes)

@app.route('/add_url', methods=['POST'])
def add_url():
    data = request.json
    new_url = data.get("url")
    if new_url:
        spotify_iframes.append(new_url)
        return jsonify({"message": "URL added successfully!", "urls": spotify_iframes})
    return jsonify({"error": "Invalid URL"}), 400

@app.route('/spotify_redirect')
def spotify_redirect():
    return redirect("https://www.spotify.com")

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    print("Received Data:", data)

    user_id = data.get("user_id")
    feedback = data.get("feedback")
    duration = data.get("duration")
    playlist = data.get("playlist")

    if not user_id or not feedback or duration is None:
        return jsonify({"message": "Invalid data"}), 400

    # Insert feedback into ListeningReport table
    new_report = ListeningReport(
        user_id=user_id,
        playlist=playlist,
        login_time=datetime.utcnow(),
        duration=int(duration),
        feedback=feedback
    )

    try:
        db.session.add(new_report)

        if feedback.lower() == "negative":
            mood_entry = Mood.query.filter_by(playlist=playlist).first()

            if mood_entry:
                print(f"Before Update: Negative Feedback Count = {mood_entry.negative_feedback_count}")

                if mood_entry.negative_feedback_count is None:
                    mood_entry.negative_feedback_count = 0

                mood_entry.negative_feedback_count += 1  # Increment feedback count
                db.session.commit()  # Save increment

                print(f"After Update: Negative Feedback Count = {mood_entry.negative_feedback_count}")

                # Format age group properly
                mood_entry_age_group = mood_entry.age_group.replace("-", " to ")

                # Debugging: Print available ModifyPlaylist records
                print(f"Searching ModifyPlaylist for mood='{mood_entry.mood}', age_group='{mood_entry_age_group}'")
                playlists = ModifyPlaylist.query.all()
                for p in playlists:
                    print(f"ID: {p.id}, Mood: {p.mood}, Age Group: {p.age_group}, URL: {p.playlist_url}")

                # Check if count has reached 2
                if mood_entry.negative_feedback_count >= 2:
                    new_playlist = ModifyPlaylist.query.filter(
                        ModifyPlaylist.mood.ilike(mood_entry.mood),
                        ModifyPlaylist.age_group.ilike(mood_entry_age_group)
                    ).first()

                    if new_playlist:
                        print(f"Updating playlist to: {new_playlist.playlist_url}")

                        mood_entry.playlist = new_playlist.playlist_url
                        mood_entry.negative_feedback_count = 0  # Reset count
                        db.session.commit()  # Save playlist update
                    else:
                        print("No replacement playlist found in ModifyPlaylist.")

        print("Feedback saved successfully!")
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error saving feedback:", str(e))
        return jsonify({"message": "Database error"}), 500

    return jsonify({"message": "Feedback saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
