#!/usr/bin/env python
import getpass
import threading
import queue
from screen_controller.virtual_display import Display
import tkinter as tk


class VirtualScreenDrawer(threading.Thread):

    def __init__(self, command_q):
        super(VirtualScreenDrawer, self).__init__()
        self.command_q = command_q
        self.stop_request = threading.Event()
        self.root = None
        self.display = None

    def callback(self):
        self.root.quit()

    def join(self, timeout=None):
        self.stop_request.set()
        super(VirtualScreenDrawer, self).join(timeout)

    def run(self):
        # init tkinter
        self.root = tk.Tk()
        self.display = Display(self.root)
        self.display.grid()

        # run mainloop and check queue
        while not self.stop_request.isSet():
            try:
                self.root.update()
                command = self.command_q.get(True, 0.05)
                print(command)
                if isinstance(command, tuple):
                    self.draw(command[0], command[1])
                elif isinstance(command, bool) and command:
                    self.turn_display_off()

            except queue.Empty:
                continue

    def draw(self, image, rgb):
        self.display.set_screen(image, rgb)
        self.root.update()
        pass

    def turn_display_off(self):
        pass
