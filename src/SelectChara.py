import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil, zipfile
from datetime import datetime

class SelectChara:
    def __init__(self, parent, data):
        self.window = tk.Toplevel(parent)
        self.window.transient(parent)
        self.window.grab_set()

        self.bgcolor = "#f7f7f7"
        self.bgcolor = "#1e1e1e"


        self.window.title("Note de counterplay")
        self.window.geometry("610x610")
        self.window.configure(bg=self.bgcolor)

        self.photos = []

        self.pseudo = data[0]
        self.perso = data[1]
        self.perso_img = data[2]

        self.adversaire = None
        self.adversaire_img = None
        
        self.build_ui()


    def build_ui(self):
        i=0
        j=0
        for file in os.listdir("assets/icons"):
            if ".jpg" in file:
                img = Image.open(f"assets/icons/{file}")
                img = img.resize((96,96))
                photo = ImageTk.PhotoImage(img)
                self.photos.append(photo) 
                l = tk.Label(self.window, image=photo)
                l.grid(column=i, row=j, padx=2, pady=2)
                l.bind('<Button-1>', lambda e, f=file: self.on_chara_click(e, f))
                i+=1
                if i>5:
                    i=0
                    j+=1


    def on_chara_click(self, event, file):
        self.adversaire= file.split(".")[0]
        self.window.destroy()
