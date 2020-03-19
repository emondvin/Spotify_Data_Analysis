import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import numpy as np

# Authorization Code Flow: Enter your credentials below.

client_id ='ID'
client_secret = 'SECRET'
username = 'USER' # Your Spotify username

scope = 'user-library-read playlist-modify-public playlist-read-private'
    #for avaliable scopes see https://developer.spotify.com/web-api/using-scopes/

redirect_uri= 'https://developer.spotify.com/dashboard/applications/144c271440e34fb48a19ffaeeb540243'
    # Paste your Redirect URI here

client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret =client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

#-------------------------------------------------------------------------
def get_artist(artist):
    """Return the artist name, popularity, and uri from spotify catalogue"""
    search = sp.search(artist, type = 'artist')
    artist_name = search['artists']['items'][0]['name']
    artist_uri = search['artists']['items'][0]['uri']
    artist_popularity = search['artists']['items'][0]['popularity']
    artist_genre = search['artists']['items'][0]['genres']
    result = [artist_name, artist_popularity, artist_uri, artist_genre]

    return result



def get_albums(artist_uri):
    """Return dataframe of studio album names, popularity,
        and uri's from artist's discography"""
    albums_search = sp.artist_albums(artist_uri, album_type = 'album')
    albums_search['items'][0]

    albums = []
    album_uris = []
    album_popularity = []
    album_genres = []

    for i in range(len(albums_search['items'])):
        albums.append(albums_search['items'][i]['name'])
        album_uris.append(albums_search['items'][i]['uri'])
        album_popularity.append(sp.album(albums_search['items'][i]['uri'])['popularity'])

    albums_df = pd.DataFrame(
    {'albums': albums, 'album_popularity': album_popularity, 'album_uri': album_uris}
    )

    return albums_df
    # return albums, album_uris, album_popularity


def get_top_tracks(artist_uri):
    """Returns the artists top ten tracks and features for each song"""

    top_tracks_raw = sp.artist_top_tracks(artist_uri)['tracks']

    top_tracks = []
    track_uris  = []

    for i in range(len(top_tracks_raw)):
        top_tracks.append(top_tracks_raw[i]['name'])
        track_uris.append(top_tracks_raw[i]['uri'])

    features = []
    for i in range(len(top_tracks_raw)):
        audio_features = sp.audio_features(track_uris[i])[0]
        popularity = {'popularity': sp.track(track_uris[i])['popularity']}
            # Popularity not included in audio features, get it from track function
        audio_features = dict(audio_features, **popularity)
        features.append(audio_features)

    top_tracks_df = pd.DataFrame(features, index = top_tracks)
    top_tracks_df = top_tracks_df[['id', 'popularity', 'acousticness',
    'danceability', 'duration_ms', 'energy','instrumentalness', 'key',
    'liveness', 'loudness', 'speechiness', 'tempo','time_signature', 'valence' ]]

    return top_tracks_df

# -----------------------------------------------------------------------------------
