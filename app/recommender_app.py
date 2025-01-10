import sys

sys.path.append(".")

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import pandas as pd
from utils.functions import get_song_recommendations, search_track_info


# Load data with caching for better performance
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/clean/7_clustered_dataset.csv")
    except FileNotFoundError:
        st.error("The dataset file could not be found. Please check the file path.")
        return pd.DataFrame()  # Return an empty DataFrame if file not found


# Load the dataset
songs_df = load_data()


# Function to get song details by title
def get_song_details(title, df):
    # First, try to get the song details from the dataset
    result = df[df["title"].str.lower() == title.lower()]

    # If the song is found in the dataset, return it
    if isinstance(result, pd.DataFrame) and not result.empty:
        return result
    else:
        # If the song is not found, call the function to search on Spotify
        spotify_data = search_track_info(
            title
        )  # Ensure this function is correctly defined and imported

        if spotify_data is not None:
            # Assuming spotify_data is a dictionary or some structure that contains necessary details
            # Convert spotify data into a pandas DataFrame format that matches your dataset structure
            spotify_df = pd.DataFrame([spotify_data])
            return spotify_df
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no data is found


# Function to get recommendations based on cluster
# def get_recommendations(title, artist, genres, df):
#     """
#     Get song recommendations based on title, artist, and genres.
#     """
#     # Initialize an empty DataFrame for recommendations
#     recommendations = pd.DataFrame()

#     # First, try to find recommendations based on genres
#     if genres:
#         recommendations = df[
#             df["genres"].str.contains("|".join(genres), case=False, na=False)
#             & (df["title"].str.lower() != title.lower())
#         ]
#         st.write(f"Recommendations found based on genres: {recommendations.shape[0]}")

#     # If no recommendations found based on genres, try by artist
#     if recommendations.empty and artist:
#         recommendations = df[
#             (df["artist"].str.lower() == artist.lower())
#             & (df["title"].str.lower() != title.lower())
#         ]
#         st.write(f"Recommendations found based on artist: {recommendations.shape[0]}")

#     # If still no recommendations, try by title similarity (fuzzy matching)
#     if recommendations.empty:
#         recommendations = df[
#             df["title"].str.contains(title, case=False, na=False)
#             & (df["title"].str.lower() != title.lower())
#         ]
#         st.write(
#             f"Recommendations found based on title similarity: {recommendations.shape[0]}"
#         )

#     # If still no recommendations, try to find songs in the same cluster (if applicable)
#     if recommendations.empty:
#         # Get the cluster of the original song if available
#         song_row = df[df["title"].str.lower() == title.lower()]
#         if not song_row.empty:
#             cluster = song_row.iloc[0].get("cluster", None)
#             if cluster is not None:
#                 recommendations = df[
#                     (df["cluster"] == cluster)
#                     & (df["title"].str.lower() != title.lower())
#                 ]
#                 st.write(
#                     f"Recommendations found based on cluster: {recommendations.shape[0]}"
#                 )

#     # Limit to 10 recommendations
#     recommendations = recommendations.head(10)


#     return recommendations
def get_recommendations(df):
    """
    Get 5 random song recommendations.
    """
    # Randomly sample 5 recommendations from the DataFrame
    recommendations = df.sample(
        n=5, random_state=1
    )  # Set random_state for reproducibility

    return recommendations


def display_recommendations(recommendations):
    """
    Display the recommendations with album cover, title, artist, and release date.
    """
    if not recommendations.empty:
        st.write("### Recommended Songs:")
        for idx, row in recommendations.iterrows():
            col1, col2 = st.columns([1, 3])  # Create two columns for layout
            with col1:
                if row.get("album_cover"):
                    st.image(row["album_cover"], width=100)  # Display album cover
                else:
                    st.write("No album cover available.")
            with col2:
                st.markdown(f"**{row['title']}**")
                st.markdown(f"*{row['artist']}*")
                if "album" in row and row["album"] != "Unknown":
                    st.markdown(f"Album: {row['album']}")
                if "year" in row and row["year"] != "Unknown":
                    st.markdown(f"**Release Year**: {row['year']}")
    else:
        st.write("No recommendations found.")


def display_song_details(song_row):
    """
    Display the details of a song including title, artist, album, and album cover.
    """
    # Ensure that necessary columns exist in the song_row before accessing them
    song_name = song_row.get("title", "Unknown")
    artist_name = song_row.get("artist", "Unknown")
    album = song_row.get("album", "Unknown")  # Default to 'Unknown' if not found
    release_year = song_row.get("year", "Unknown")  # Default to 'Unknown' if not found
    album_cover = song_row.get("album_cover", None)

    # Display song details
    col1, col2 = st.columns([1, 3])
    with col1:
        if album_cover:
            st.image(album_cover, width=180)
        else:
            st.write("No album cover available.")
    with col2:
        st.markdown(f"### {song_name}")
        st.markdown(f"*{artist_name}*")
        st.markdown(f"Album: {album}")
        if release_year != "Unknown":
            st.markdown(f"**Release Year**: {release_year}")


# Reset the session state variables for new input
def reset_session_state():
    st.session_state["submit_pressed"] = False
    st.session_state["selected_song"] = None


# Pre-fill the input field with the suggested song
def prefill_input(user_input, songs_df):
    suggestions = songs_df[
        songs_df["title"].str.contains(user_input[:3], case=False, na=False)
    ].head(1)
    if not suggestions.empty:
        st.session_state["user_input"] = suggestions.iloc[0]["title"]
    else:
        st.session_state["user_input"] = ""  # Clear input if no suggestion is found


# Initialize session state for button handling
if "submit_pressed" not in st.session_state:
    st.session_state["submit_pressed"] = False
if "selected_song" not in st.session_state:
    st.session_state["selected_song"] = None


# Streamlit app UI
col1, col2 = st.columns([2, 7])
with col1:
    st.image("assets/k-recs_logo02.svg", width=350)

st.title("A Song Recommender App!")
st.write("Hi there! Welcome to the K-Recs Song Recomender.")
st.write("Give us a song, and we’ll find recommendations for you. 🎵")

# Input field for song title
user_input = st.text_input(
    "Enter your song title:",
    placeholder="Your song title - e.g., Jingle Bells",
    label_visibility="hidden",
)

# Submit button
if st.button("Submit"):
    st.session_state["submit_pressed"] = True
    st.session_state["selected_song"] = user_input

# If the Submit button was pressed
if st.session_state["submit_pressed"]:
    user_input = st.session_state["selected_song"]
    if user_input:
        # Get song details
        song_row = get_song_details(user_input, songs_df)
        if not song_row.empty:
            # Display song details
            display_song_details(song_row.iloc[0])

            # Ask if this is the correct song
            st.write("---")
            st.write("Is this the correct song?")
            col_yes, col_no = st.columns(2)

            with col_yes:
                if st.button("Yes, this is the one!", key="yes_button"):
                    # Get random recommendations
                    recommended_songs = get_recommendations(
                        songs_df
                    )  # Call with only the DataFrame

                    # Display the recommendations
                    display_recommendations(recommended_songs)

            with col_no:
                if st.button("No, re-enter input", key="no_button"):
                    # Reset session state and pre-fill input
                    reset_session_state()
                    prefill_input(user_input, songs_df)

        else:
            st.write(f"Sorry, '{user_input}' not found in the database.")
            suggestions = songs_df[
                songs_df["title"].str.contains(user_input[:3], case=False, na=False)
            ].head(5)
            if not suggestions.empty:
                st.write("Did you mean:")
                for suggestion in suggestions["title"]:
                    st.markdown(f"- {suggestion}")
            else:
                st.write("Please enter something before submitting.")
