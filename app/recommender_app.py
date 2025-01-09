import streamlit as st
import pandas as pd

@st.cache
def load_data():
    return pd.read_csv('data/clean/7_clustered_dataset.csv')

songs_df = load_data()

# songs_df = pd.read_csv('data/clean/7_clustered_dataset.csv')

# Streamlit app UI
st.title("Hello!")
st.write("Hi there! Welcome to the Streamlit app.")
st.write("This is gonna be a song recommender.")

# Input field for song title
user_input = st.text_input("Enter a song title:")

# Button
if st.button('Submit'):
    print('submit button pressed')
    if user_input:
        # Check if the input matches any song title in the 'title' column of the DataFrame
        song_row = songs_df[songs_df['title'].str.lower() == user_input.lower()]
        
        if not song_row.empty:
            song_name = song_row.iloc[0]['title']
            artist_name = song_row.iloc[0]['artist']
            
            # Handle release_year (ensure it's correctly formatted)
            release_year = song_row.iloc[0]['year'] if 'year' in song_row.columns else 'Unknown'
            
            album_cover = song_row.iloc[0]['album_cover'] if 'album_cover' in song_row.columns else None
            song_cluster = song_row.iloc[0]['cluster'] if 'cluster' in song_row.columns else None
            
            # Debug statements
            st.write("### Debug Information")
            st.write(f"Selected Song: {song_name}")
            st.write(f"Artist: {artist_name}")
            st.write(f"Release Year: {release_year}")
            st.write(f"Cluster: {song_cluster}")
            st.write("---")
            
            # Create two columns for the layout
            col1, col2 = st.columns([1, 3])  # The album cover column is smaller (1), and the song details column is larger (3)
            
            with col1:
                # Display album cover if available
                if album_cover:
                    st.image(album_cover, caption=f"Album Cover for {song_name}", width=100)  # Set width to make it smaller
                else:
                    st.write("No album cover available.")
            
            with col2:
                # Display song details (title, artist, release year)
                st.markdown(f"### {song_name}")
                st.markdown(f"**Artist**: {artist_name}")
                st.markdown(f"**Release Year**: {release_year}")
            
            # Ask if this is the correct song with a unique key
            if st.button("Yes, this is the one!", key='yes_button'):
                st.write("Yes button pressed")
                st.write(f"Great! You selected '{song_name}' by {artist_name}.")
                if song_cluster is not None:
                    # Recommend songs from the same cluster
                    recommended_songs = songs_df[songs_df['cluster'] == song_cluster]
                    recommended_songs = recommended_songs[recommended_songs['title'].str.lower() != song_name.lower()]  # Exclude the selected song
                    print('song cluster is not none')
                    # Debug statement
                    st.write(f"Number of recommended songs found: {recommended_songs.shape[0]}")
                    print('some songs to recommend were found')
                    
                    # Display recommended songs
                    if not recommended_songs.empty:
                        st.write("### Recommended Songs:")
                        for idx, row in recommended_songs.iterrows():
                            st.markdown(f"**{row['title']}**")  # Only display the title
                            # Optional: To display more details, uncomment below
                            # st.markdown(f"**{row['title']}** by {row['artist']} ({row['release_year']})")
                            # st.image(row['album_cover'], caption=f"Album Cover for {row['title']}", width=50)
                    else:
                        st.write("No other songs found in the same cluster.")
                else:
                    st.write("Cluster information is missing for the selected song.")
            
            if st.button("No, re-enter input", key='no_button'):
                st.write("'No' button pressed")
                st.experimental_rerun()
        else:
            st.write(f"Sorry, '{user_input}' not found in the database.")
    else:
        st.write("Please enter something before submitting.")