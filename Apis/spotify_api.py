import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
from Apis.config_loader import load_config
from datetime import datetime, timedelta


class Song:
    def __init__(self, artist, album, track, left_time, is_playing):
        self.is_playing = is_playing
        self.artist = self.parse_string(artist)
        self.album = self.parse_string(album)
        self.track = self.parse_string(track)
        self.left_time = left_time

    @staticmethod
    def parse_string(string):
        if string.split("("):
            return string.split("(")[0]
        return string

    def __str__(self):
        if self.is_playing:
            return self.track + " from " + self.artist + " on the album " + self.album
        else:
            return "Song is not playing"


class SpotifyApi:

    def __init__(self):
        self.config = load_config()
        self.oauth_client = self._get_oauth_client()

    def _get_oauth_client(self):
        client_id = self.config['spotify']['clientId']
        client_secret = self.config['spotify']['clientSecret']
        redirect_uri = self.config['spotify']['redirectURI']
        scope = self.config['spotify']['tokenScope']
        cache_path = self.config['spotify']['cache']
        return oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, cache_path=cache_path, scope=scope)

    def _get_access_token(self):
        token_info = self.oauth_client.get_cached_token()

        if token_info:
            if self.oauth_client.is_token_expired(token_info):
                token_info = self.oauth_client.refresh_access_token(token_info['refresh_token'])
                return token_info['access_token']
            return token_info['access_token']
        else:
            return self._get_first_access_token()

    def _get_first_access_token(self):
        username = self.config['spotify']['username']
        client_id = self.config['spotify']['clientId']
        client_secret = self.config['spotify']['clientSecret']
        redirect_uri = self.config['spotify']['redirectURI']
        scope = self.config['spotify']['tokenScope']
        cache_path = self.config['spotify']['cache']

        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri,
                                           cache_path=cache_path)
        if token:
            return token
        else:
            print("Can't get token for", username)
            raise Exception("AuthenticationException", "Spotify couldn't get token")

    def get_current_song(self):
        sp = spotipy.Spotify(auth=self._get_access_token())
        result = sp.current_playback()
        if result and result['is_playing'] and result['currently_playing_type'] == 'track':
            artist = result['item']['artists'][0]['name']
            is_playing = result['is_playing']
            album = result['item']['album']['name']
            track = result['item']['name']
            left_time = datetime.now() + timedelta(
                milliseconds=int(result['item']['duration_ms']) - int(result['progress_ms']))
            return Song(artist, album, track, left_time, True)
        else:
            return Song("playing", "", "No Song", 0, False)

    def skip_song(self):
        sp = spotipy.Spotify(auth=self._get_access_token())
        sp.next_track()

    def previous_song(self):
        sp = spotipy.Spotify(auth=self._get_access_token())
        sp.previous_track()

    def toggle_playback(self):
        sp = spotipy.Spotify(auth=self._get_access_token())
        song = self.get_current_song()
        if song and song.is_playing:
            sp.pause_playback()
        else:
            sp.start_playback()  # no active device found

if __name__ == '__main__':
    d = SpotifyApi()
    d.pause()
