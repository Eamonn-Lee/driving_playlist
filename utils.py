import time
import spotipy

def spot(sp_func, *args, **kwargs):
    """
    Helper function for calling spotify via spotipy
    Handles HTTP 429 rate limits
    """
    retries = 3
    while retries > 0:
        try:
            return sp_func(*args, **kwargs)
        
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After', 5))
                print(f"Rate limit hit. Wait {retry_after} secs before retry")
                time.sleep(retry_after)
                retries -= 1
            else:
                raise e
            
    raise Exception("Spotify API rate limit exceeded. Please try again later.")
