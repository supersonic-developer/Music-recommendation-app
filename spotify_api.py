import spotipy
import json
import os
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAPI:
    def __init__(self, num_of_recommendations=5):
        self.client_id = '21f92c97d58e4bf4ac44199f64c69185'
        self.client_secret = '7c1eccf7a2644c67a1c4488918c78c46'
        self.redirect_uri = 'http://localhost:8080/callback'
        self.scope = 'user-library-read playlist-read-private playlist-read-collaborative'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope))       
        self.num_of_recommendations = num_of_recommendations
        self.available_genres = []
        self.liked_songs = []

    def get_liked_songs(self):
        # If the liked songs have already been fetched, return them
        if self.liked_songs:
            return self.liked_songs
        
        # Check if the liked songs are available in a local file and the file was modified today
        if os.path.exists('data/liked_songs.json') and datetime.fromtimestamp(os.path.getmtime('data/liked_songs.json')).date() == datetime.today().date():
            with open('data/liked_songs.json', 'r') as f:
                tracks_ids = json.load(f)
        else:
            # If the liked songs are not available locally or the file was not modified today, fetch them from the Spotify API
            tracks_ids = []
            results = self.sp.current_user_saved_tracks(limit=50)
            while results:
                tracks_ids.extend([item['track']['id'] for item in results['items']])
                if results['next']:
                    results = self.sp.next(results)
                else:
                    results = None

            # Update the JSON file with the new list of liked songs
            with open('data/liked_songs.json', 'w') as f:
                json.dump(tracks_ids, f)

        self.liked_songs = tracks_ids
        return tracks_ids

    def extract_track_data(self, results):
        tracks_data = []
        for track in results['tracks']:
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            formatted_data = f"{track_name} - {artist_name}"
            tracks_data.append(formatted_data)
        return tracks_data
    
    def get_song_id(self, song_name):
        results = self.sp.search(q=song_name, limit=1, type='track')
        items = results['tracks']['items']
        if items:
            returned_song_name = items[0]['name']
            if song_name.lower() not in returned_song_name.lower():
                warning = f"Warning: Search query '{song_name}' does not match returned track name '{returned_song_name}'."
            else:
                warning = None
            return items[0]['id'], warning
        else:
            warning = f"Warning: No song found for search query '{song_name}'."
            return None, warning
        
    def get_artist_id(self, artist_name):
        results = self.sp.search(q=artist_name, limit=1, type='artist')
        items = results['artists']['items']
        if items:
            returned_artist_name = items[0]['name']
            if artist_name.lower() not in returned_artist_name.lower():
                warning = f"Warning: Search query '{artist_name}' does not match returned track name '{returned_artist_name}'."
            else:
                warning = None
            return items[0]['id'], warning
        else:
            warning = f"Warning: No artist found for search query '{artist_name}'."
            return None, warning

    def get_recommendations_based_on_song(self, song_id):
        results = self.sp.recommendations(seed_tracks=[song_id], limit=self.num_of_recommendations)
        tracks_data = self.extract_track_data(results)
        track_ids = [track['id'] for track in results['tracks']]
        return tracks_data, track_ids
    
    def get_recommendations_based_on_artist(self, artist_id):
        results = self.sp.recommendations(seed_artists=[artist_id], limit=self.num_of_recommendations)
        tracks_data = self.extract_track_data(results)
        track_ids = [track['id'] for track in results['tracks']]
        return tracks_data, track_ids
    
    def get_recommendations_based_on_genre(self, genre):
        results = self.sp.recommendations(seed_genres=[genre], limit=self.num_of_recommendations)
        tracks_data = self.extract_track_data(results)
        track_ids = [track['id'] for track in results['tracks']]
        return tracks_data, track_ids
    
    def get_available_genres(self):
        # Create the data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')

        # Check if the genres are available in a local file
        if os.path.exists('data/genres.json'):
            with open('data/genres.json', 'r') as f:
                genres = json.load(f)
        else:
            # If the genres are not available locally, make a request to the Spotify API
            results = self.sp.recommendation_genre_seeds()
            genres = results['genres']

            # Store the genres in a local file for future use
            with open('data/genres.json', 'w') as f:
                json.dump(genres, f)
                
        self.available_genres = genres
        return genres