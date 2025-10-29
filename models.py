from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime



db = SQLAlchemy()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Increase to 255
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)
    profile_pic = db.Column(db.String(200))  # URL of profile picture
    feedback_count = db.Column(db.Integer, default=0)
    listening_time = db.Column(db.String(20), default="0 min 0 sec")
    mood = db.Column(db.String(20), nullable=True)  # Ensure this exists
    age_group = db.Column(db.String(50))  # Add this if missing

class Mood(db.Model):
    __tablename__ = 'mood'
    
    id = db.Column(db.Integer, primary_key=True)
    age_group = db.Column(db.String(50), nullable=False)  # Define the age_group field
    mood = db.Column(db.String(50), nullable=False)
    playlist = db.Column(db.String(255), nullable=False)
    negative_feedback_count = db.Column(db.Integer, default=0)  # Track negative feedback

    
    def __init__(self, age_group, mood, playlist):
        self.age_group = age_group
        self.mood = mood
        self.playlist = playlist

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=True)

class ListeningReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    playlist = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    feedback = db.Column(db.Text, nullable=True)

class UserPlaylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'), nullable=False)
    song_url = db.Column(db.String(500), nullable=False)

class ModifyPlaylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    age_group = db.Column(db.String(20), nullable=False)
    playlist_url = db.Column(db.Text, nullable=False)
