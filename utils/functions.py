import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.cluster import KMeans
import streamlit as st


def search_track_info(input_title, input_artist):
    client_id = os.getenv("SPOTIFY_CLIENT_ID") or st.secrets["SPOTIFY_CLIENT_ID"]
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET") or st.secrets["SPOTIFY_CLIENT_SECRET"]

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    response = sp.search(q=f'track:{input_title} artist:{input_artist}', type='track', limit=1)

    if response["tracks"]["total"] == 0: return None

    track = response["tracks"]["items"][0]
    track_title = track["name"]
    track_popularity = track["popularity"]

    artist = sp.artist(track["artists"][0]["id"])
    artist_name = artist["name"]
    artist_genres = artist["genres"]

    album = sp.album(response["tracks"]["items"][0]["album"]["id"])
    album_popularity = album["popularity"]

    result = {
        "title": track_title,
        "artist": artist_name,
        "popularity": track_popularity,
        "album_popularity": album_popularity,
        "genres": artist_genres
    }

    return result

def get_song_recommendations(song_title, artist_name, n_recommendations=5):
    """
    Get song recommendations based on input song and optional artist name
    """
    df = pd.read_csv('data/5_clustered_dataset.csv')

    # Convert inputs to lowercase for matching
    song_title = song_title.strip().lower()
    artist_name = artist_name.strip().lower()

    # Find the input song on spotify
    spotify_info = search_track_info(song_title, artist_name)
    if spotify_info is None:
        return None

    # Run KMeans clustering on the result from spotify
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster = kmeans.fit_predict(df[['popularity', 'album_popularity']])

    # Get songs from the same cluster
    recommendations = df[df['cluster'] == cluster]
    recommendations = recommendations.sample(min(n_recommendations, len(recommendations)))
    
    return recommendations[['title', 'artist', 'popularity', 'album_popularity']]