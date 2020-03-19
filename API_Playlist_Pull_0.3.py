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

# ----------------------------------------------------------------------------------

def get_playlist_feats(playlist_id):
    """Retrieve the songs, their features, popularity, and related artist
        genres from a users playlists"""
    sourcePlaylistID = playlist_id
    sourcePlaylist = sp.user_playlist(username, sourcePlaylistID);
    tracks = sourcePlaylist["tracks"];
    songs = tracks["items"];

    track_ids = []
    track_names = []
    track_artists = []


    for i in range(0, len(songs)):
        if songs[i]['track']['id'] != None: # Removes the local tracks in your playlist if there is any
            track_ids.append(songs[i]['track']['id'])
            track_names.append(songs[i]['track']['name'])
            track_artists.append(songs[i]['track']['artists'])


    features = []
    for i in range(0,len(track_ids)):
        audio_features = sp.audio_features(track_ids[i])[0]
        track_popularity = {'popularity': sp.track(track_ids[i])['popularity']}
        genre = {'genres': sp.artist(track_artists[i][0]['uri'])['genres']}
        audio_features = dict(audio_features, **track_popularity, **genre)
        features.append(audio_features)


    playlist_df = pd.DataFrame(features, index = track_names)
    return playlist_df
# ------------------------------------------------------------------------------

top_2019 = get_playlist_feats('37i9dQZF1Etk7fJUDjOQfi')
top_2018 = get_playlist_feats('37i9dQZF1Ejqu2YzDW3QW7')
top_2017 = get_playlist_feats('37i9dQZF1E9WZdF5cHDFWQ')
top_2016 = get_playlist_feats('37i9dQZF1CyJXIXDWK8gIf')
top_decade = get_playlist_feats('37i9dQZF1DX2cPuVFw41Td')
top_decade_fr = get_playlist_feats('37i9dQZF1DXdDG2JPYsK5j')


files_user = [top_2019, top_2018, top_2017, top_2016, top_decade, top_decade_fr]
filenames_user = ['top_2019', 'top_2018', 'top_2017', 'top_2016', 'top_decade', 'top_decade_fr']
for i in range(len(files_user)):
    files_user[i].to_csv(r'Path\%s.csv' % filenames_user[i], index = True, header = True)

sp_top_2019 = get_playlist_feats('37i9dQZF1DXcz8eC5kMSWZ')
sp_top_2018 = get_playlist_feats('37i9dQZF1DX1HUbZS4LEyL')
sp_top_decade = get_playlist_feats('37i9dQZF1DWYJ5kmTbkZiz')
sp_top_2019_can = get_playlist_feats('37i9dQZF1DX82re5NxbwyO')

files_sp = [sp_top_2019, sp_top_2018, sp_top_decade, sp_top_2019_can]
filenames_sp = ['sp_top_2019', 'sp_top_2018', 'sp_top_decade', 'sp_top_2019_can']
for i in range(len(files_sp)):
    files_sp[i].to_csv(r'Path\%s.csv' % filenames_sp[i], index = True, header = True)


# ------------------------------------------------------------------------------
