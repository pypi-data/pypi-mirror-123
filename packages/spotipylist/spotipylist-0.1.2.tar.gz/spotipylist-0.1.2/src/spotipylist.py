import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from utils.playlist_generator import get_music_library, write_playlist

def spotipylist():
    # take input of playlist URL or playlist_id from user
    playlist_url = input("""
    Please input the desired playlist ID.\n
    The id will be the string of characters at the end of the URL as below\n
    https://open.spotify.com/playlist/5t9TUKubTd0bOriqsxq79h -> 5t9TUKubTd0bOriqsxq79h\n
    Playlist ID: """)

    # SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET need to be set via environment variables

    auth_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Get playlist_items and necessary fields (name, artists)

    results = spotify.playlist_items(
    playlist_url, 
    market="US", 
    fields="items(track(name, artists(name)))"
    )['items']

    music_library, library_artists = get_music_library()

    playlist_name = input("Name for New Playlist \
    (This will overwrite any playlist with the same name): ")

    write_playlist(results, playlist_name, music_library, library_artists)