from weather_screen import WeatherScreen
from toggl_screen import TogglScreen
import signal
import time

on_RPI = True
if on_RPI:
    from gfxhat import touch
    import screen_drawer


class Manager:

    def __init__(self):
        self.screens = [WeatherScreen(), TogglScreen()]
        self.current_screen = self.screens[0]

        if on_RPI:
            for x in range(6):
                touch.on(x, handler=self.btn_handler)
        self.event_loop()

    def btn_handler(self, channel, event):
        print("Got {} on channel {}".format(event, channel))
        if event == 'press':
            if channel == 5:
                signal.pause()
                time.sleep(5)
                self.event_loop()
                return
            touch.set_led(channel, 1)
            is_changed = self.current_screen.btn_handler(channel)
            if is_changed:
                self.push_screen()

        elif event == 'release':
            touch.set_led(channel, 0)
        
        if event == 'press' and channel == 2:
            self.current_screen = self.screens[(self.screens.index(self.current_screen) + 1)%len(self.screens)]
            self.push_screen()

    def push_screen(self):
        image, rgb = self.current_screen.get_bitmap_rgb()
        if on_RPI:
            screen_drawer.draw(image, rgb)
        else:
            image.show()

    def event_loop(self):
        try:
            while True:
                self.push_screen()
                self.current_screen.update()
        except KeyboardInterrupt:
            screen_drawer.turn_display_off()


if __name__ == '__main__':
    Manager()
