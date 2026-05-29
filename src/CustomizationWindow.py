import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil, zipfile
from datetime import datetime

class CustomizationWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.transient(parent)
        self.window.grab_set()

        self.fontsize = 12
        self.iconsize = 48
        self.ingamesize = 32
        self.dlsize = 48

        self.fgcolor = "#f7f7f7"
        self.bgcolor = "#1e1e1e"

        self.get_data()

        self.window.title("Customisation")
        self.window.geometry("400x600")
        self.window.configure(bg=self.bgcolor)

        self.build_ui()

    def get_data(self):
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
            text="Thème",
            font=("Segoe UI", 16, "bold"),
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        title.pack(pady=20)

        fg_label = tk.Label(
            self.window,
            text="Couleur du texte (Défaut: #f7f7f7):",
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        fg_label.pack(fill="x", anchor="w", padx=30)

        self.fg_entry = tk.Entry(
            self.window,
            font=("Segoe UI", 16),
            textvariable=tk.StringVar(self.window, self.fgcolor)
        )
        self.fg_entry.pack(fill="x", padx=30, pady=10)

        bg_label = tk.Label(
            self.window,
            text="Couleur du fond (Défaut: #1e1e1e):",
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        bg_label.pack(fill="x", anchor="w", padx=30)

        self.bg_entry = tk.Entry(
            self.window,
            font=("Segoe UI", 16),
            textvariable=tk.StringVar(self.window, self.bgcolor)
        )
        self.bg_entry.pack(fill="x", padx=30, pady=10)

        fontsize_label = tk.Label(
            self.window,
            text="Taille du texte (Défaut: 12):",
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        fontsize_label.pack(fill="x", anchor="w", padx=30)

        self.fontsize_entry = tk.Spinbox(
            self.window,
            from_=8,
            to=48,
            font=("Segoe UI", 16),
            textvariable=tk.StringVar(self.window, self.fontsize)
        )
        self.fontsize_entry.pack(fill="x", padx=30, pady=10)

        iconsize_label = tk.Label(
            self.window,
            text="Taille des icônes de persos (Défaut: 48):",
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        iconsize_label.pack(fill="x", anchor="w", padx=30)

        self.iconsize_entry = tk.Spinbox(
            self.window,
            from_=8,
            to=128,
            font=("Segoe UI", 16),
            textvariable=tk.StringVar(self.window, self.iconsize)
        )
        self.iconsize_entry.pack(fill="x", padx=30, pady=10)

        ingamesize_label = tk.Label(
            self.window,
            text="Taille des icônes de boutons (Défaut: 32):",
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        ingamesize_label.pack(fill="x", anchor="w", padx=30)

        self.ingamesize_entry = tk.Spinbox(
            self.window,
            from_=8,
            to=128,
            font=("Segoe UI", 16),
            textvariable=tk.StringVar(self.window, self.ingamesize)
        )
        self.ingamesize_entry.pack(fill="x", padx=30, pady=10)

        dlsize_label = tk.Label(
            self.window,
            text="Taille des icônes de moves (Défaut: 48):",
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        dlsize_label.pack(fill="x", anchor="w", padx=30)

        self.dlsize_entry = tk.Spinbox(
            self.window,
            from_=8,
            to=128,
            font=("Segoe UI", 16),
            textvariable=tk.StringVar(self.window, self.dlsize)
        )
        self.dlsize_entry.pack(fill="x", padx=30, pady=10)

        save_btn = ttk.Button(
            self.window,
            text="Sauvegarder",
            command=self.save_theme
        )
        save_btn.pack(pady=20)

    def save_theme(self):

        self.fgcolor = self.fg_entry.get()
        self.bgcolor = self.bg_entry.get()
        self.fontsize = self.fontsize_entry.get()
        self.iconsize = self.iconsize_entry.get()
        self.ingamesize = self.ingamesize_entry.get()
        self.dlsize = self.dlsize_entry.get()

        with open("data/theme.data","wb") as f:
            f.write(f"{self.fgcolor}\n{self.bgcolor}\n{self.fontsize}\n{self.iconsize}\n{self.ingamesize}\n{self.dlsize}".encode())
            f.close()        

        messagebox.showinfo(
            "Theme",
            "Theme sauvegardé !"
        )

        self.window.destroy()
        self.window.master.event_generate("<<THEME_UPDATED>>")