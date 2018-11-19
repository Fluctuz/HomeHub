import getpass
from queue import Queue

on_RPI = getpass.getuser() == "pi"

if on_RPI:
    from screen_controller.gfx_drawer import GfxDrawer
    from gfxhat import touch
else:
    from screen_controller.virtual_screen_drawer import VirtualScreenDrawer


class ScreenController:

    def __init__(self, manager):
        if on_RPI:
            for x in range(6):
                touch.on(x, handler=manager.btn_handler)
        else:
            self.command_q = Queue()
            self.screen_drawer = VirtualScreenDrawer(self.command_q)
            self.screen_drawer.start()

    def draw(self, image, rgb=(0, 100, 0)):
        if on_RPI:
            GfxDrawer.draw(image, rgb)
        else:
            self.command_q.put_nowait((image,rgb))

    def turn_display_off(self):
        if on_RPI:
            GfxDrawer.turn_display_off()
        else:
            self.command_q.put_nowait(True)

