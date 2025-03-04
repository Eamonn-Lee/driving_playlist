# Fresh Spotify Playlist Generator For Driving

A modular Python application that creates or updates a Spotify playlist based on your recently liked songs and recommendations. It uses the Spotify API via Spotipy and adapts to the current situation by leveraging the `/search` endpoint to simulate recommendations.

## Features

- **Authentication**: Uses Spotify OAuth to securely authenticate and authorize your account.
- **Seed Track Selection**: Retrieves your 20 most recently liked songs and selects 2 most recent plus 3 additional random tracks as seed tracks.
- **Recommendations via Search**: Uses the currently playing track’s artist and title to search for similar tracks. Filters out duplicates and excludes any tracks with the same name as the currently playing track. Optionally retrieves the seed artist’s genres and filters search results to ensure recommendations match the seed artist's musical style.
- **Playlist Management**: Checks if a playlist named "Generated Playlist" exists on your profile. If it exists, it clears and updates it; if not, it creates a new playlist. Supports both public and private playlists (ensure you have the correct scopes).

## Prerequisites

- Python 3.7 or later
- Spotipy

## Usage
Before usage, set up spotify credentials:
Create a file named `config.json` in the root directory with your Spotify API credentials. This file should be added to `.gitignore`.

   **Example `config.json`:**
   ```json
   {
       "client_id": "your_spotify_client_id",
       "client_secret": "your_spotify_client_secret",
       "redirect_uri": "http://localhost:8888/callback"
   }
   ```

To run the application, execute:

```sh
python main.py
```

Upon execution, the script will:

1. Authenticate with Spotify.
2. Retrieve your liked songs and grab seed tracks.
3. Use the `/search` endpoint to find recommendations based on the seed track and its artist’s genre.
4. Create or update the "Generated Playlist" on your Spotify profile with the new tracks.
   

## File Structure

- `spotify_auth.py`: Loads Spotify credentials from `config.json` and creates an authenticated Spotipy client.
- `utils.py`: Provides helper functions (e.g., `spot()`) to handle API calls and rate limits.
- `seed_tracks.py`: Retrieves the user's recently liked songs and selects seed tracks.
- `recommended_tracks.py`: Uses the `/search` endpoint to generate recommended tracks, filtering duplicates and non-matching genres.
- `playlist_manager.py`: Creates or updates the playlist ("FreshPlaylist") on your Spotify profile with the selected tracks.
- `main.py`: Orchestrates the modules: authentication, seed track selection, recommendation generation, and playlist update.


## License

This project is open source and available under the MIT License.

## Acknowledgements

- [Spotipy Documentation](https://spotipy.readthedocs.io/)
- [Spotify Developer Documentation](https://developer.spotify.com/)
