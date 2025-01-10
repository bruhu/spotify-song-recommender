import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
from utils.functions import get_song_recommendations

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
    return df[df['title'].str.lower() == title.lower()]

# Function to get recommendations based on cluster
def get_recommendations(cluster, df, exclude_title):
    return df[(df['cluster'] == cluster) & (df['title'].str.lower() != exclude_title.lower())]

def display_song_details(song_row):
    """
    Display the details of a song including title, artist, album, and album cover.
    """
    song_name = song_row['title']
    artist_name = song_row['artist']
    album = song_row['album']
    release_year = song_row.get('year', 'Unknown')
    album_cover = song_row.get('album_cover', None)

    # Display song details
    col1, col2 = st.columns([1, 3])
    with col1:
        if album_cover:
            st.image(album_cover, width=150)
        else:
            st.write("No album cover available.")
    with col2:
        st.markdown(f"### {song_name}")
        st.markdown(f"*{artist_name}*")
        st.markdown(f"Album: {album}")
        if release_year != 'Unknown':
            st.markdown(f"**Release Year**: {release_year}")

# Reset the session state variables for new input
def reset_session_state():
    st.session_state['submit_pressed'] = False
    st.session_state['selected_song'] = None

# Pre-fill the input field with the suggested song
def prefill_input(user_input, songs_df):
    suggestions = songs_df[songs_df['title'].str.contains(user_input[:3], case=False, na=False)].head(1)
    if not suggestions.empty:
        st.session_state['user_input'] = suggestions.iloc[0]['title']
    else:
        st.session_state['user_input'] = ""  # Clear input if no suggestion is found

# Initialize session state for button handling
if 'submit_pressed' not in st.session_state:
    st.session_state['submit_pressed'] = False
if 'selected_song' not in st.session_state:
    st.session_state['selected_song'] = None



# Streamlit app UI
col1, col2 = st.columns([2, 7]) 
with col1:
    st.image("assets/k-recs_logo02.svg", width=350)

st.title("A Song Recommender App!")
st.write("Hi there! Welcome to the K-Recs Song Recomender.")
st.write("Give us a song, and we’ll find recommendations for you. 🎵")

# Input field for song title
user_input = st.text_input("Enter your song title:", placeholder="Your song title - e.g., Jingle Bells", label_visibility="hidden")

# Submit button
if st.button('Submit'):
    st.session_state['submit_pressed'] = True
    st.session_state['selected_song'] = user_input

# If the Submit button was pressed
if st.session_state['submit_pressed']:
    user_input = st.session_state['selected_song']
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
                if st.button("Yes, this is the one!", key='yes_button'):
                    song_cluster = song_row.iloc[0].get('cluster', None)
                    if song_cluster is not None:
                        recommended_songs = get_recommendations(song_cluster, songs_df, song_row.iloc[0]['title'])
                        if not recommended_songs.empty:
                            st.write("### Recommended Songs:")
                            cols = st.columns(3)
                            for idx, row in recommended_songs.iterrows():
                                with cols[idx % 3]:
                                    st.image(row['album_cover'], caption=row['title'], width=100)
                                    st.write(f"**Artist**: {row['artist']}")
                        else:
                            st.write("No other songs found in the same cluster.")
                    else:
                        st.write("Cluster information is missing for the selected song.")
            
            with col_no:
                if st.button("No, re-enter input", key='no_button'):
                    # Reset session state and pre-fill input
                    reset_session_state()
                    prefill_input(user_input, songs_df)
        
        else:
            st.write(f"Sorry, '{user_input}' not found in the database.")
            suggestions = songs_df[songs_df['title'].str.contains(user_input[:3], case=False, na=False)].head(5)
            if not suggestions.empty:
                st.write("Did you mean:")
                for suggestion in suggestions['title']:
                    st.markdown(f"- {suggestion}")
            else:
                st.write("Please enter something before submitting.")