import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil, zipfile
from datetime import datetime

class ProfileWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.transient(parent)
        self.window.grab_set()

        self.fontsize = 12
        self.iconsize = 48
        self.ingamesize = 32
        self.dlsize = 48

        self.bgcolor = "#f7f7f7"
        self.bgcolor = "#1e1e1e"

        self.pseudo = None
        self.perso = None
        self.perso_img = None

        self.get_data()

        self.window.title("Profil utilisateur")
        self.window.geometry("400x500")
        self.window.configure(bg=self.bgcolor)


        self.opt = tk.StringVar(value=self.perso)


        
        self.build_ui()

    def get_data(self):
        if os.path.exists("data/profile.data"):
            with open("data/profile.data", "rb") as f:
                data = f.readlines()
                if len(data)<2:
                    self.pseudo = data
                else:
                    self.pseudo = data[0].decode().strip()
                    self.perso = data[1].decode().strip()
                exte = ".jpg"
                if not self.perso:
                    self.perso = "default"
                    exte = ".png"
                self.perso_img = f"assets/icons/{self.perso}{exte}"

        if os.path.exists("data/theme.data"):
            with open("data/theme.data", "rb") as f:
                data = f.readlines()
                self.fgcolor = data[0].strip()
                self.bgcolor = data[1].strip()
                self.fontsize = int(data[2].strip())
                self.iconsize = int(data[3].strip())
                self.ingamesize = int(data[4].strip())
                self.dlsize = int(data[5].strip())

    def build_ui(self):

        title = tk.Label(
            self.window,
            text="Profil",
            font=("Segoe UI", self.fontsize, "bold"),
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        title.pack(pady=20)

        pseudo_label = tk.Label(
            self.window,
            text="Pseudo :",
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        pseudo_label.pack(fill="x", anchor="w", padx=30)

        self.pseudo_entry = tk.Entry(
            self.window,
            font=("Segoe UI", self.fontsize),
            textvariable=tk.StringVar(self.window, self.pseudo)
        )
        self.pseudo_entry.pack(fill="x", padx=30, pady=10)

        
        main_label = tk.Label(
            self.window,
            text="Main GGST :",
            bg="#1e1e1e",
            fg="white"
        )
        main_label.pack(anchor="w", padx=30)

        self.main_dropdown = tk.OptionMenu(
            self.window, 
            self.opt, 
            *charas
        )  
        self.main_dropdown.pack(anchor="w", padx=30, pady=10)


        self.main_dropdown.config(
            font=("Segoe UI", self.fontsize),
            width=30
        )

        save_btn = ttk.Button(
            self.window,
            text="Sauvegarder",
            command=self.save_profile
        )
        save_btn.pack(pady=20)

    def save_profile(self):

        self.pseudo = self.pseudo_entry.get()
        self.perso = self.opt.get()

        if not os.path.exists(f"profiles/{self.pseudo}"):
            os.makedirs(f"profiles/{self.pseudo}")
        if not os.path.exists(f"profiles/{self.pseudo}/{self.perso}"):
            os.makedirs(f"profiles/{self.pseudo}/{self.perso}")
            os.makedirs(f"profiles/{self.pseudo}/{self.perso}/roundstart")
            os.makedirs(f"profiles/{self.pseudo}/{self.perso}/counterplay")
            os.makedirs(f"profiles/{self.pseudo}/{self.perso}/uniques")
            os.makedirs(f"profiles/{self.pseudo}/{self.perso}/random")
        with open("data/profile.data","wb") as f:
            f.write(f"{self.pseudo}\n{self.perso}".encode())
            f.close()        

        messagebox.showinfo(
            "Profil",
            "Profil sauvegardé !"
        )

        self.window.destroy()
        self.window.master.event_generate("<<PROFILE_UPDATED>>")
