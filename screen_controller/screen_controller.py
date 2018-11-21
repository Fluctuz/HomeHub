import getpass
on_RPI = getpass.getuser() == "pi"

if on_RPI:
    from screen_controller.gfx_drawer import GfxDrawer
    from gfxhat import touch
else:
    from screen_controller.virtual_screen_drawer import VirtualScreenDrawer
    from queue import Queue


class ScreenController:

    def __init__(self, manager):
        self.manager = manager
        if on_RPI:
            for x in range(6):
                touch.on(x, handler=self.manager.btn_handler)
        else:
            self.command_q = Queue()
            self.screen_drawer = VirtualScreenDrawer(self.command_q, self.manager.btn_handler)
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

