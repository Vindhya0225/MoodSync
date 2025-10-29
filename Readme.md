🎧 MoodSync – AI-Powered Mood-Based Music Application
MoodSync is an intelligent music application that curates playlists based on the user’s current mood.
It combines AI-driven sentiment analysis, Spotify playlist integration, and user feedback learning to deliver a personalized, adaptive music experience.

⚙️ Core Concept
MoodSync provides two ways for users to access mood-based music:
- Manual Mood Selection
Users manually select their mood (e.g., happy, sad, calm, energetic).
The system instantly fetches and plays a matching Spotify playlist.

- Chat-Based Mood Detection (Gemini AI)
Users chat with an integrated Gemini AI chatbot.
The chatbot analyzes the conversation using sentiment analysis to detect the user’s emotional tone.
Based on the detected mood, MoodSync recommends an appropriate Spotify playlist.

- Profile & Personalization
Every listening session is logged:
Mood detected or selected
Playlist recommended
Duration of listening
User feedback (how well the playlist matched their mood)
This data is displayed on the Profile Page and used to continuously update and refine future playlist suggestions, ensuring music that evolves with the user’s preferences.

⚙️ Tech Stack
- Frontend:
HTML
CSS
Bootstrap

- Backend:
Flask (API & mood tracking logic)
Gemini AI (for Chatbot)
Rule based NLP for sentiment analysis
Spotify API (to fetch playlists based on detected mood)

- Database:
PostgreSQL (for storing user profiles, feedback, and session data)

⚙️ Workflow
- User logs in and chooses to either select a mood manually or chat with the Gemini AI.
- The system detects and confirms the mood.
- A Spotify playlist matching that mood is fetched and played.
- Before exiting, the user gives feedback and the listening duration is recorded.
- MoodSync stores all data and learns user preferences to improve future recommendations.

⚙️ Future Enhancements
-Integrate facial emotion detection for automatic mood capture.
-Introduce personalized playlist generation using listening history.
-Add weekly mood-music analytics on the profile dashboard.
-Train a personalised AI model integrated with NLP 