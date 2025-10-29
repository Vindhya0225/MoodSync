from flask import Blueprint, request, jsonify
from textblob import TextBlob
from models import Mood  # ✅ Import Mood model
from flask import Flask, render_template, request, jsonify

routes = Blueprint('routes', __name__)

@routes.route('/test', methods=['GET'])
def test_route():
    return {"message": "Routes file is working!"}

@routes.route('/api/get_playlist', methods=['GET'])
def get_playlist():
    mood = request.args.get('mood')
    age = request.args.get('age', type=int)  # Convert age to integer

    # Determine the correct age group
    if 14 <= age <= 30:
        age_group = "14-30"
    elif 31 <= age <= 55:
        age_group = "31-55"
    else:
        age_group = "56+"

    print(f"Received Mood: {mood}, Age: {age}, Mapped Age Group: {age_group}")

    # Fetch playlist for the selected mood and age group
    mood_entry = Mood.query.filter_by(mood=mood, age_group=age_group).first()

    if mood_entry:
        print(f"Found Playlist: {mood_entry.playlist}")
        return jsonify({'playlist': mood_entry.playlist})
    else:
        print("No playlist found for this mood and age group.")
        return jsonify({'error': 'No playlist found'}), 404


