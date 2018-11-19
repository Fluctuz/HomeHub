import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
import time


class Display(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.down_button = tk.Button(self, text="v", height=7)
        self.up_button = tk.Button(self, text="\u1d27", height=7)
        self.switch_button = tk.Button(self, text="<", height=4)
        self.plus_button = tk.Button(self, text="+", width=10)
        self.circular_button = tk.Button(self, text="\u2295", width=10)
        self.minus_button = tk.Button(self, text="-", width=10)

        self.root = root
        self.screen = tk.Canvas(self, height=256, width=512)
        self.back_l = tk.Canvas(self, height=256, width=40)

        self.screen.grid(row=0, column=1, rowspan=3, columnspan=3)
        self.back_l.grid(row=0, column=4, rowspan=3)
        self.up_button.grid(row=0, column=0)
        self.down_button.grid(row=1, column=0)
        self.switch_button.grid(row=2, column=0)

        self.minus_button.grid(row=3, column=1)
        self.circular_button.grid(row=3, column=2)
        self.plus_button.grid(row=3, column=3)

        self.down_button.bind("<ButtonPress>", lambda event: self.on_btn_handler(0, 'press'))
        self.down_button.bind("<ButtonRelease>", lambda event: self.on_btn_handler(0, 'release'))

    def on_btn_handler(self, channel, event):
        print("ON BTN PRESSED")
        t = Image.new('P', (128, 64))
        draw = ImageDraw.Draw(t)
        draw.rectangle([(0, 0), t.size], fill=(255, 255, 0))
        self.set_screen(t)

    def set_screen(self, bitmap, rgb):
        image = bitmap.resize((512, 256))
        back_l_image = Image.new("RGB", (40, 256), rgb)

        self.root.back_l = ImageTk.PhotoImage(back_l_image)
        self.root.screen = ImageTk.PhotoImage(image)
        self.screen.create_image(0, 0, image=self.root.screen, anchor='nw')
        self.back_l.create_image(0,0, image=self.root.back_l, anchor='nw')

if __name__ == "__main__":
    root = tk.Tk()
    display = Display(root)
    display.grid()
    t = Image.new('P', (128, 64))
    draw = ImageDraw.Draw(t)
    draw.rectangle([(0, 0), t.size], fill=(255, 255, 0))
    display.set_screen(t)
    root.update()
    time.sleep(10)
    root.update()
