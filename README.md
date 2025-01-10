# K-Recs Song Recommender App

## Description
K-Recs is a song recommender application that allows users to input a song title and receive recommendations based on the song's characteristics. The app utilizes a dataset of songs with various features and integrates with the Spotify API to fetch additional song details.

## Features
- Input a song title to receive recommendations.
- Displays song details including title, artist, album, and album cover.
- Provides recommendations based on genres, artist, and release year.
- User-friendly interface built with Streamlit.

## Technologies Used
- Python
- Streamlit
- Pandas
- Spotipy (for Spotify API integration)
- dotenv (for environment variable management)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/k-recs.git
   cd k-recs
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Spotify API credentials:
   - Create a `.env` file in the root directory of the project.
   - Add your Spotify API credentials:
     ```
     SPOTIFY_CLIENT_ID=your_client_id
     SPOTIFY_CLIENT_SECRET=your_client_secret
     ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app/recommender_app.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. Enter a song title in the input field and click "Submit" to receive recommendations.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the Spotify API for providing access to song data.
- Thanks to the Streamlit community for creating an easy-to-use framework for building web apps.