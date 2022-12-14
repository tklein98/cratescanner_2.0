# MOVE TO METADATA FOLDER
from os.path import join, dirname
from os import environ
import os
from dotenv import load_dotenv, find_dotenv
from crate_scanner.getmusicdata.spotifyapi import SpotifyAPI


env_path = join(dirname(dirname(dirname(__file__))), ".env")
load_dotenv(find_dotenv())
#load_dotenv(dotenv_path=env_path)
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

spotify = SpotifyAPI(client_id, client_secret)


def get_album(artist):
    # Grab the relevant album metadata json file based on album_id from Spotify API
    album_search = spotify.search(query = artist, search_type="album")
    try:
        return album_search['albums']['items'][0]
    except:
        return None


def get_album_by_track_id(track_id):
    # Grab the relevant album json file based on track_id from Spotify API
    album_search = spotify.get_track_by_id(track_id)["album"]
    if len(album_search)>0:
        return album_search['id']
    else:
        return None


def get_track_from_album(album):
    #Use API search query to extract the first song from the given album_id
    album_search = spotify.get_tracks_from_album_id(album)
    try:
        return album_search["tracks"]['items'][0]["id"]
    except:
        return None


def get_track_audio_features(track_id):
  # Use API search query to extract audio features of a song based on track_id
    try:
        return spotify.query_track_audio_features(track_id)
    except:
        return None

# if __name__ == "__main__":
#   print(client_id, client_secret)
#   print(env_path)
