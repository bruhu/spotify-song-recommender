import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.cluster import KMeans
import streamlit as st


def search_track_info(input_title):
    """Fetch song details from Spotify including song title, album cover, album name, release date, and genres."""

    # Get Spotify client credentials from environment or secrets
    client_id = os.getenv("SPOTIFY_CLIENT_ID") or st.secrets["SPOTIFY_CLIENT_ID"]
    client_secret = (
        os.getenv("SPOTIFY_CLIENT_SECRET") or st.secrets["SPOTIFY_CLIENT_SECRET"]
    )

    # Initialize Spotipy with client credentials
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
    )

    # Perform track search on Spotify using the input song title
    try:
        response = sp.search(q=f"track:{input_title}", type="track", limit=1)
    except Exception as e:
        st.error(f"Error fetching data from Spotify: {e}")
        return None

    # Return None if no tracks are found
    if response["tracks"]["total"] == 0:
        return None

    # Extract track details
    track = response["tracks"]["items"][0]
    track_title = track["name"]
    track_popularity = track["popularity"]

    # Fetch artist details
    artist = sp.artist(track["artists"][0]["id"])
    artist_name = artist["name"]
    artist_genres = artist.get("genres", [])

    # Fetch album details
    album = track["album"]["name"]
    release_date = track["album"]["release_date"]
    album_cover = (
        track["album"]["images"][1]["url"]
        if len(track["album"]["images"]) > 1
        else None
    )  # Fallback if no image

    # Construct the result dictionary with the requested fields
    result = {
        "title": track_title,
        "artist": artist_name,
        "album": album,
        "album_cover": album_cover,
        "year": release_date,
        "genres": artist_genres,  # Include genres if needed
    }
    return result


# def get_song_recommendations(song_title, artist_name, df, n_recommendations=5):
#     """
#     Get song recommendations based on input song and optional artist name.
#     Assumes 'df' is a DataFrame containing clustered song data.
#     """
#     # Convert inputs to lowercase for matching
#     song_title = song_title.strip().lower()
#     artist_name = artist_name.strip().lower()

#     # Find the input song in the dataframe (matching both song title and artist name)
#     song_row = df[(df['title'].str.lower() == song_title) & (df['artist'].str.lower() == artist_name)]

#     if song_row.empty:
#         return None  # No match found

#     # Run KMeans clustering on the result
#     kmeans = KMeans(n_clusters=3, random_state=42)
#     cluster = kmeans.fit_predict(df[['popularity', 'album_popularity']])

#     # Get songs from the same cluster as the input song
#     song_cluster = song_row.iloc[0]['cluster']
#     recommendations = df[df['cluster'] == song_cluster]

#     # Sample 'n_recommendations' songs from the cluster
#     recommendations = recommendations.sample(min(n_recommendations, len(recommendations)))

#     return recommendations[['title', 'artist', 'popularity', 'album_popularity']]


def get_song_recommendations(song_title, artist_name, df, n_recommendations=5):
    """
    Get song recommendations based on the input song and optional artist name.
    Assumes 'df' is a DataFrame containing song data with relevant columns.
    """
    # Convert inputs to lowercase for matching
    song_title = song_title.strip().lower()
    artist_name = artist_name.strip().lower()

    # Find the input song in the dataframe (matching both song title and artist name)
    song_row = df[
        (df["title"].str.lower() == song_title)
        & (df["artist"].str.lower() == artist_name)
    ]

    if song_row.empty:
        return None  # No match found

    # Get the cluster of the input song
    song_cluster = song_row.iloc[0]["cluster"]

    # Get songs from the same cluster as the input song (excluding the input song itself)
    recommendations = df[
        (df["cluster"] == song_cluster)
        & (df["title"].str.lower() != song_title.lower())
    ]

    # Sample 'n_recommendations' songs from the cluster
    recommendations = recommendations.sample(
        min(n_recommendations, len(recommendations))
    )

    # Return the recommended songs with relevant details (title, artist, album cover, release date, popularity)
    recommendations = recommendations[
        ["title", "artist", "album_cover", "album_release_date", "popularity", "genres"]
    ]

    # Simplify the 'album_release_date' to just year for display purposes
    recommendations["release_year"] = recommendations["album_release_date"].apply(
        lambda x: (
            datetime.strptime(x, "%Y-%m-%d").year
            if isinstance(x, str) and x != "Unknown"
            else "Unknown"
        )
    )

    return recommendations[
        ["title", "artist", "album_cover", "release_year", "popularity", "genres"]
    ]
