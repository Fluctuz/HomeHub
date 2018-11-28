from Screens.screen import ScreenHandler
from Apis.spotify_api import SpotifyApi
from PIL import Image, ImageDraw
import time
from datetime import datetime


class SpotifyScreen(ScreenHandler):

    def __init__(self, main_loop):
        super().__init__(main_loop)
        self.spotify = SpotifyApi()
        self.font = super().get_font("pixelmix", 10)
        self.current_song = self.spotify.get_current_song()

    def btn_handler(self, channel):
        if channel <= 2:
            return False
        if channel == 3:
            self.spotify.previous_song()
            self.current_song = self.spotify.get_current_song()
            self.main_loop.wait(1)
        elif channel == 4:
            self.spotify.toggle_playback()
            self.current_song = self.spotify.get_current_song()
            self.main_loop.wait(1)
        elif channel == 5:
            self.spotify.skip_song()
            self.main_loop.wait(1)
            self.current_song = self.spotify.get_current_song()

        return True

    def get_bitmap_rgb(self):
        if self.current_song.is_playing:
            file_name = "pause.bmp"
        else:
            file_name = "play.bmp"

        playback_icon = Image.open("Assets/media_playback_icons/" + file_name).resize((25, 25)).convert("1")
        skip_icon = Image.open("Assets/media_playback_icons/skip.bmp").resize((25, 25)).convert("1")
        previous_icon = Image.open("Assets/media_playback_icons/previous.bmp").resize((25, 25)).convert("1")

        image = Image.new('P', super().dimension())
        draw = ImageDraw.Draw(image)

        draw.text((10, 5), self.current_song.track, 200, self.font)
        draw.text((10, 25), self.current_song.artist, 200, self.font)

        draw.bitmap((2, 40), previous_icon, 200)
        draw.bitmap((50, 40), playback_icon, 200)
        draw.bitmap((102, 40), skip_icon, 200)

        return image, (10, 90, 40)

    def update(self):
        if self.current_song.is_playing:
            if datetime.now() > self.current_song.left_time:
                self.current_song = self.spotify.get_current_song()
            self.main_loop.wait(4)
        else:
            self.main_loop.wait(60)
            self.current_song = self.spotify.get_current_song()
