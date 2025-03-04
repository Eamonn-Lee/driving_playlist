import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPE = "user-library-read playlist-modify-public playlist-modify-private playlist-read-private"
REDIRECT_URI = 'http://localhost:8888/callback'

def load_config():
    """Load user credentials from config.json."""
    with open('config.json') as config_file:
        return json.load(config_file)

def get_spotify_client():
    """Authenticate with Spotify, return spotipy client."""
    config = load_config()
    
    auth_manager = SpotifyOAuth(
        client_id = config["SPOTIFY_CLIENT_ID"],
        client_secret = config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
    return spotipy.Spotify(auth_manager=auth_manager)
