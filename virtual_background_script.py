import tkinter as tk
import sys
import subprocess
import os


#pid = subprocess.Popen([sys.executable,"manager.py"])
#out, err = pid.communicate()
#print(out)
#print(err)
if False:
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()


    def start_manager():
        subprocess.Popen([sys.executable, "/home/fluctuz/HomeHub/manager.py"])
       # root.destroy()


    button = tk.Button(frame,
                       text="QUIT",
                       fg="red",
                       command=quit)
    button.pack(side=tk.LEFT)
    slogan = tk.Button(frame,
                       text="Start Manager",
                       command=start_manager)
    slogan.pack(side=tk.LEFT)

    root.mainloop()