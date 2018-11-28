from Screens.weather_screen import WeatherScreen
from Screens.toggl_screen import TogglScreen
from Screens.todoist_screen import TodoistScreen
from Screens.spotify_screen import SpotifyScreen
from screen_controller.screen_controller import ScreenController
import getpass
import threading
import signal

on_RPI = getpass.getuser() == "pi"
if on_RPI:
    from gfxhat import touch


class Manager:
    def __init__(self):
        self.screen_controller = ScreenController(self)
        self.main_loop = threading.Event()
        self.screens = [WeatherScreen(self.main_loop), TogglScreen(self.main_loop),
                        TodoistScreen(self.main_loop), SpotifyScreen(self.main_loop)]
        self.current_screen = self.screens[0]
        self.is_main_loop = threading.Event()
        self.is_main_loop.set()
        self.is_screen_off = False
        self.event_loop()

    @staticmethod
    def turn_off_led(channel):
        touch.set_led(channel, 0)

    def btn_handler(self, channel, event):
        #print("Got {} on channel {}".format(event, channel))

        #Handle LED
        if event == 'press' and on_RPI:
            touch.set_led(channel, 1)
            threading.Timer(0.5, self.turn_off_led, [channel]).start()

        # Turn Script off
        if channel == 0 and event == 'press' and isinstance(self.current_screen, WeatherScreen):
            self.toggle_screen()
            return

        # Pass to screen
        if event == 'press':
            is_changed = self.current_screen.btn_handler(channel)
            if is_changed:
                self.main_loop.set()
                self.main_loop.clear()

        # Change Screens
        if event == 'press' and channel == 2:
            self.current_screen = self.screens[(self.screens.index(self.current_screen) + 1) % len(self.screens)]
            self.push_screen()

    def toggle_screen(self):
        # Turn off
        print(self.current_screen)
        if not self.is_screen_off:
            self.is_screen_off = True
            self.screen_controller.turn_display_off()
            self.is_main_loop.clear()
            self.main_loop.set()
            self.main_loop.clear()
        # Turn On
        else:
            self.is_screen_off = False
            self.is_main_loop.set()
        return False

    def push_screen(self):
        image, rgb = self.current_screen.get_bitmap_rgb()
        self.screen_controller.draw(image, rgb)

    def event_loop(self):
        try:
            while True:
                if self.is_main_loop.is_set():
                    try:
                        self.push_screen()
                        self.current_screen.update()
                    except:
                        pass
                else:
                    self.is_main_loop.wait(1000)
        except KeyboardInterrupt:
            print("Turn Screen Off")
            self.screen_controller.turn_display_off()


if __name__ == '__main__':
    Manager()
