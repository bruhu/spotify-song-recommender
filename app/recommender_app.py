import streamlit as st
import pandas as pd

songs_df = pd.read_csv('data/clean/7_clustered_dataset.csv')

# Streamlit app UI
st.title("Hello!")
st.write("Hi there! Welcome to the Streamlit app.")
st.write("This is gonna be a song recommender.")

# Input field for song title
user_input = st.text_input("Enter a song title:")

# Button
if st.button('Submit'):
    if user_input:
        # Check if the input matches any song title in the 'title' column of the DataFrame
        song_row = songs_df[songs_df['title'].str.lower() == user_input.lower()]
        
        if not song_row.empty:
            song_name = song_row.iloc[0]['title']
            artist_name = song_row.iloc[0]['artist']
            release_year = song_row.iloc[0]['release_year']
            album_cover = song_row.iloc[0]['album_cover']
            song_cluster = song_row.iloc[0]['cluster']  # Get the cluster of the selected song
            
            # Create two columns for the layout
            col1, col2 = st.columns([1, 3])  # The album cover column is smaller (1), and the song details column is larger (3)
            
            with col1:
                # Display album cover
                st.image(album_cover, caption=f"Album Cover for {song_name}", width=100)  # Set width to make it smaller
            
            with col2:
                # Display song details (title, artist, release year)
                st.markdown(f"### {song_name}")
                st.markdown(f"**Artist**: {artist_name}")
                st.markdown(f"**Release Year**: {release_year}")
            
            # Ask if this is the correct song
            if st.button("Yes, this is the one!"):
                st.write(f"Great! You selected '{song_name}' by {artist_name}.")
                
                # Recommend songs from the same cluster
                recommended_songs = songs_df[songs_df['cluster'] == song_cluster]
                recommended_songs = recommended_songs[recommended_songs['title'] != song_name]  # Exclude the selected song
                
                # Display recommended songs
                if not recommended_songs.empty:
                    st.write("### Recommended Songs:")
                    for idx, row in recommended_songs.iterrows():
                        st.markdown(f"**{row['title']}** by {row['artist']} ({row['release_year']})")
                        st.image(row['album_cover'], caption=f"Album Cover for {row['title']}", width=50)
                else:
                    st.write("No other songs found in the same cluster.")
            elif st.button("No, re-enter input"):
                st.text_input("Re-enter the song title:")
        else:
            st.write(f"Sorry, '{user_input}' not found in the database.")
    else:
        st.write("Please enter something before submitting.")