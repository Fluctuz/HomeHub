from weather_screen import WeatherScreen
from toggl_screen import TogglScreen

on_RPI = True
if on_RPI:
    from gfxhat import touch
    import screen_drawer


class Manager:

    def __init__(self):
        self.screens = [WeatherScreen(), TogglScreen()]
        self.current_screen = self.screens[0]

        if on_RPI:
            touch.on(1, handler=self.btn_handler)

        self.event_loop()

    def btn_handler(self, channel, event):
        print("Got {} on channel {}".format(event, channel))
        if event == 'press' and channel == 2:
            self.current_screen = self.screens[(self.screens.index(self.current_screen) + 1)%len(self.screens) - 1]

    def event_loop(self):
        try:
            while True:
                image, rgb = self.current_screen.get_bitmap_rgb()
                if on_RPI:
                    screen_drawer.draw(image, rgb)
                else:
                    image.show()
                self.current_screen.update()
        except KeyboardInterrupt:
            screen_drawer.turn_display_off()


if __name__ == '__main__':
    Manager()
