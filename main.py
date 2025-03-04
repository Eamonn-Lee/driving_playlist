from spotify_auth import get_spotify_client
from seed_tracks import get_seeds
from recommended_tracks import get_recommended_tracks
from playlist_manager import create_update_playlist
from utils import spot

def main():
    # Auth client
    sp = get_spotify_client()
    
    user = spot(sp.current_user)
    user_id = user["id"]

    # Get seed recommendation tracks from liked songs
    seed_tracks = get_seeds(sp)

    # Gen recommendations from seeds
    recommended_tracks = get_recommended_tracks(sp, seed_tracks)

    # Combine seeds and recommendations
    seed_track_ids = [track["id"] for track in seed_tracks]
    final_track_ids = []
    for tid in seed_track_ids + recommended_tracks:
        if tid not in final_track_ids:
            final_track_ids.append(tid)

    # Gen new playlist
    create_update_playlist(sp, user_id, final_track_ids)

if __name__ == "__main__":
    main()
