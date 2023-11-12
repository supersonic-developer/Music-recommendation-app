import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAPI:
    def __init__(self, num_of_recommendations=5):
        self.client_id = '21f92c97d58e4bf4ac44199f64c69185'
        self.client_secret = '7c1eccf7a2644c67a1c4488918c78c46'
        self.redirect_uri = 'http://localhost:8080/callback'
        self.scope = 'user-library-read playlist-read-private playlist-read-collaborative'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope))
        #self.available_genres = self.get_available_genres()
        self.available_genres = []
        self.num_of_recommendations = num_of_recommendations

    def get_liked_songs(self):
        results = self.sp.current_user_saved_tracks(limit=50)
        tracks_data = self.extract_track_data(results)
        return tracks_data

    def extract_track_data(self, results):
        tracks_data = []
        i = 0
        for track in results['tracks']:
            i += 1
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            formatted_data = f"{i}. {track_name} - {artist_name}"
            tracks_data.append(formatted_data)
        return tracks_data
    
    def get_recommendations_based_on_liked_songs(self):
        liked_song_ids = self.get_liked_songs()
        recommendations = []
        for song_id in liked_song_ids:
            results = self.sp.recommendations(seed_tracks=[song_id])
            tracks_data = self.extract_track_data(results)
            recommendations.extend(tracks_data)
        return recommendations
    
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

    def get_recommendations_based_on_song(self, song_id):
        results = self.sp.recommendations(seed_tracks=[song_id], limit=self.num_of_recommendations)
        tracks_data = self.extract_track_data(results)
        return tracks_data
    
    def get_recommendations_based_on_genre(self, genre):
        results = self.sp.recommendations(seed_genres=[genre], limit=self.num_of_recommendations)
        tracks_data = self.extract_track_data(results)
        return tracks_data
    
    def get_available_genres(self):
        results = self.sp.recommendation_genre_seeds()
        return results['genres']