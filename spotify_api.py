import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAPI:
    def __init__(self):
        self.client_id = '21f92c97d58e4bf4ac44199f64c69185'
        self.client_secret = '7c1eccf7a2644c67a1c4488918c78c46'
        self.redirect_uri = 'http://localhost:8080/callback'
        self.scope = 'user-library-read playlist-read-private playlist-read-collaborative'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope))

    def get_liked_songs(self):
        results = self.sp.current_user_saved_tracks(limit=50)
        tracks_data = self.extract_track_data(results)
        return tracks_data

    def extract_track_data(self, results):
        tracks_data = []
        for item in results['items']:
            track = item['track']
            track_id = track['name']
            tracks_data.append(track_id)
        return tracks_data
    
    def get_recommendations_based_on_liked_songs(self):
        liked_song_ids = self.get_liked_songs()
        recommendations = []
        for song_id in liked_song_ids:
            results = self.sp.recommendations(seed_tracks=[song_id])
            tracks_data = self.extract_track_data(results)
            recommendations.extend(tracks_data)
        return recommendations