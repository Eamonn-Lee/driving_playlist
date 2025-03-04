import random
from utils import spot

def get_seeds(sp, limit=20):
    """
    Retrieve:
    - The 2 most recent liked songs
    - 3 additional randomly selected liked songs from the remaining list

    Returns list of dicts with detailed track info.
    """

    results = spot(sp.current_user_saved_tracks, limit=limit)
    saved_tracks = results["items"]

    if len(saved_tracks) < 5:
        raise Exception("Not enough liked songs to generate recommendations. Please like more songs.")

    seed_tracks = []

    # select 2 most recent liked songs
    for item in saved_tracks[:2]:
        track = item["track"]
        seed_tracks.append({
            "id": track["id"],
            "name": track["name"],
            "artists": track["artists"],
            "album": track["album"]["name"]
        })

    # select 3 random tracks from the remaining liked songs
    remaining_tracks = saved_tracks[2:]
    if len(remaining_tracks) >= 3:
        additional_items = random.sample(remaining_tracks, 3)
    else:
        additional_items = remaining_tracks

    for item in additional_items:
        track = item["track"]
        seed_tracks.append({
            "id": track["id"],
            "name": track["name"],
            "artists": track["artists"],
            "album": track["album"]["name"]
        })

    # Print seeds
    print("Selected seed tracks:")
    for track in seed_tracks:
        print(f"ID: {track['id']}, Name: {track['name']}, Artists: {', '.join([artist['name'] for artist in track['artists']])}")
    
    return seed_tracks
