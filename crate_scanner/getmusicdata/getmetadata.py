# MOVE TO METADATA FOLDER
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv
from crate_scanner.getmusicdata.spotifyapi import SpotifyAPI


env_path = join(dirname(dirname(dirname(__file__))), ".env")
load_dotenv(dotenv_path=env_path)

client_id = environ.get('SPOTIFY_CLIENT_ID')
client_secret = environ.get('SPOTIFY_CLIENT_SECRET')

spotify = SpotifyAPI(client_id, client_secret)


def get_album(artist):

    # Grab the relevant album metadata json file based on album_id from Spotify API
    album_search = spotify.search(query = artist, search_type="album")['albums']['items']
    if len(album_search)>0:
        return album_search[0]
    else:
        return None


def get_album_by_track_id(track_id):
    # Grab the relevant album json file based on track_id from Spotify API
    album_search = spotify.get_track_by_id(track_id)["album"]
    if len(album_search)>0:
        return album_search['id']
    else:
        return None
