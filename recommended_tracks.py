import spotipy
from utils import spot
from pprint import pprint

def validate_seed_tracks(sp, seed_tracks):
    """
    Validate seed id's, if invalid print all info
    - mostly to handle local file tracks
    return list of valid seeds
    """
    valid = []
    for track in seed_tracks:
        track_id = track["id"]
        try:
            # Check track exists
            spot(sp.track, track_id)
            valid.append(track_id)
        except spotipy.exceptions.SpotifyException as e:
            # Print invalid id track
            print("Skipping invalid seed track:")
            print(f"  ID: {track_id}")
            print(f"  Name: {track.get('name', 'N/A')}")
            print(f"  Artists: {', '.join(track.get('artists', []))}")
            print(f"  Album: {track.get('album', 'N/A')}")
            print(f"  Error: {e}")
    return valid

def get_recommended_tracks(sp, seed_tracks, limit=20, market="from_token"):
    """
    Generate recommended tracks from seed after validation
    'market' parameter ensures regionally appropriate
    """

    valid_seeds = validate_seed_tracks(sp, seed_tracks)
    
    if not valid_seeds: # ensure 1 valid seed
        raise Exception("No valid seed tracks found for generating recommendations.")
    
    """ DEPRECATED: spotify API removed recommended tracks Endpoint
    valid_seeds = valid_seeds[:5]

    recommendations = spot(
        sp.recommendations,
        seed_tracks=valid_seeds,
        limit=limit,
        market=market
    )
    recommended_track_ids = [track["id"] for track in recommendations["tracks"]]
    """

    recommended_tracks = []

    for seed in seed_tracks:
        recommended_tracks += recommendations(sp, seed)

    recommended_track_ids = [track["id"] for track in recommended_tracks]   #pulling id's

    return recommended_track_ids


# Custom recommendations function due to spotify deprecation of recommendations
def recommendations(sp, seed, limit=10):
    """
    Custom recommendations algorithm:
    - when searching for a Songname + artist, get adjacent songs.
    - songs are added if they are by the same first artist or same genre of songs performed by artist/s
    Returns full song information dictionary
    """
    print("-------")
    genres = set()

    artist_name = seed["artists"][0]["name"] # Taking the first artist
    track_name = seed["name"]

    genres.update(track_to_genre(sp, seed)) # Set current song genres

    query = f"{artist_name} {track_name}"
    print(f"Searching for recommendations: '{query} - {genres}'")

    results = sp.search(q=query, type="track", limit=limit)
    tracks = results.get("tracks", {}).get("items", [])
    
    # remove any copies of songs returned in search
    seen_names = {track_name}   
    unique_tracks = []
    
    for track in tracks:
        tname = track["name"]
        if tname not in seen_names:
            unique_tracks.append(track)
            seen_names.add(tname)

    # Adding song if similar artist or genre
    recommended_tracks = []
    for track in unique_tracks:
        rtrack_genres = track_to_genre(sp, track)

        if any(genre in rtrack_genres for genre in genres) or artist_name in [artist['name'] for artist in track['artists']]: #any matching genres or same artist
            print(f"Added: Name: {track['name']}, Artists: {', '.join(artist['name'] for artist in track['artists'])} - {rtrack_genres}")
            genres.update(rtrack_genres)    # add any new genres encountered
            recommended_tracks.append(track)

    return recommended_tracks

# given a track, return the genres the artists are associated with
def track_to_genre(sp, track):
    genres = []
    for artist in track.get("artists", []):
        artist_info = sp.artist(artist.get("id"))
        genres += artist_info.get("genres", [])
    return genres