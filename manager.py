from Screens.weather_screen import WeatherScreen
from Screens.toggl_screen import TogglScreen
from Screens.todoist_screen import TodoistScreen
from screen_controller.screen_controller import ScreenController

on_RPI = False
if on_RPI:
    from gfxhat import touch
else:
    pass


class Manager:

    def __init__(self):
        self.screen_controller = ScreenController(self)
        self.screens = [WeatherScreen(), TogglScreen(), TodoistScreen()]
        self.current_screen = self.screens[0]
        self.event_loop()

    def btn_handler(self, channel, event):
        print("Got {} on channel {}".format(event, channel))
        if event == 'press':
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
        print("PUT")
        self.screen_controller.draw(image, rgb)

    def event_loop(self):
        try:
            while True:
                self.push_screen()
                self.current_screen.update()
        except KeyboardInterrupt:
            self.screen_controller.turn_display_off()


if __name__ == '__main__':
    Manager()
