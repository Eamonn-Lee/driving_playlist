from utils import spot

def create_update_playlist(sp, user_id, track_ids, playlist_name="FreshPlaylist", public=False):
    """
    check if playlist with given name exists:
      - if true, clear playlist to update
      - if false, create new
    Update playlist with recommended
    """
    existing = False

    # check for existing
    playlists_data = spot(sp.current_user_playlists, limit=50)
    playlists = playlists_data["items"]
    playlist_id = None

    for playlist in playlists:
        if playlist["name"] == playlist_name:
            playlist_id = playlist["id"]
            existing = True
            break

    if playlist_id:
        # clear playlist
        spot(sp.playlist_replace_items, playlist_id, [])
    else:
        new_playlist = spot(
            sp.user_playlist_create, user_id, playlist_name, public=public,
            description="Automatically generated playlist based on liked songs."
        )
        playlist_id = new_playlist["id"]

    # add tracks in batches of 100 - API limitation
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        spot(sp.playlist_add_items, playlist_id, batch)

    print("FreshPlaylist updated successfully" if existing else "New FreshPlaylist generated")
