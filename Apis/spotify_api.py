import json
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util


class Song:
    def __init__(self, artist, album, track, is_playing):
        self.is_playing = is_playing
        self.artist = artist
        self.album = album
        self.track = track

    def __str__(self):
        if self.is_playing:
            return self.track + " from " + self.artist + " on the album " + self.album
        else:
            return "Song is not playing"


class SpotifyApi:
    CONFIG_FILENAME = "config.json"

    def __init__(self):
        self.config = self.load_config()
        self.oauth_client = self.get_oauth_client()

    def load_config(self):
        with open(self.CONFIG_FILENAME, 'r') as f:
            return json.load(f)

    def save_config(self):
        with open(self.CONFIG_FILENAME, "w") as f:
            f.write(json.dumps(self.config))

    def get_oauth_client(self):
        client_id = self.config['spotify']['clientId']
        client_secret = self.config['spotify']['clientSecret']
        redirect_uri = self.config['spotify']['redirectURI']
        scope = self.config['spotify']['tokenScope']
        cache_path = self.config['spotify']['cache']
        return oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, cache_path=cache_path, scope=scope)

    def get_access_token(self):
        token_info = self.oauth_client.get_cached_token()

        if token_info:
            if self.oauth_client.is_token_expired(token_info):
                token_info = self.oauth_client.refresh_access_token(token_info['refresh_token'])
                return token_info['access_token']
            return token_info['access_token']
        else:
            return self.get_first_access_token()

    def get_first_access_token(self):
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
        sp = spotipy.Spotify(auth=self.get_access_token())
        result = sp.current_playback()

        if result and result['is_playing'] and result['currently_playing_type'] == 'track':
            artist = result['item']['artists'][0]['name']
            is_playing = result['is_playing']
            album = result['item']['album']['name']
            track = result['item']['name']
            return Song(artist, album, track, True)
        else:
            return Song("", "", "", False)

    def skip_song(self):
        sp = spotipy.Spotify(auth=self.get_access_token())
        sp.next_track()

    def previous_song(self):
        sp = spotipy.Spotify(auth=self.get_access_token())
        sp.previous_track()

    def toggle_playback(self):
        sp = spotipy.Spotify(auth=self.get_access_token())
        song = self.get_current_song()
        if song and song.is_playing:
            sp.pause_playback()
        else:
            sp.start_playback() #no active device found


if __name__ == '__main__':
    d = SpotifyApi()
    d.pause()
