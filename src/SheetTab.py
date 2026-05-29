import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil, zipfile
from datetime import datetime

class SheetTab:
    def __init__(self, notebook, title="Nouvelle table", rows=8, columns=8, chara_1=None, chara_2=None):
        self.frame = ttk.Frame(notebook)

        self.fontsize = 12
        self.iconsize = 48
        self.ingamesize = 32
        self.dlsize = 48

        self.fgcolor = "#f7f7f7"
        self.bgcolor = "#1e1e1e"

        self.chara_1 = chara_1
        self.chara_2 = chara_2

        self.get_data()

        self.rows = rows
        self.columns = columns
        
        self.grid_entries = {}
        self.filepath = None
        self.build_ui()

    def build_ui(self):
        for i in range(self.rows):
            self.frame.rowconfigure(i, weight=1)
        for j in range(self.columns):
            self.frame.columnconfigure(j, weight=1)

        for i in range(self.rows):
            for j in range(self.columns):
                if i == 0 and j == 0:
                    cell_frame = tk.Frame(self.frame, bg=self.bgcolor, relief="solid", borderwidth=1)
                    cell_frame.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                    cell_frame.grid_propagate(False)
                    cell_frame.pack_propagate(False)

                    t = tk.Text(
                        cell_frame,
                        fg=self.fgcolor,
                        bg=self.bgcolor,
                        font=('Segoe UI', self.fontsize, 'bold'),
                        insertbackground="white",
                        relief="flat",
                        wrap="word"
                    )
                    t.pack(fill="both", expand=True)
                    t.insert("1.0", f"{self.chara_2} →\n↓ {self.chara_1}")
                    
                    self.grid_entries[(i, j)] = t
                    
                    t.bind("<KeyRelease>", lambda event, widget=t: self.check_cell_color(widget, is_text=True))
                    t.bind("<BackSpace>", lambda event, widget=t: self.force_on_delete(widget, is_text=True))
                    t.bind("<Delete>", lambda event, widget=t: self.force_on_delete(widget, is_text=True))
                else:
                    e = tk.Entry(
                        self.frame, 
                        width=15, 
                        fg=self.fgcolor, 
                        bg=self.bgcolor,
                        font=('Segoe UI', self.fontsize, 'bold'),
                        relief="solid",
                        borderwidth=1,
                        insertbackground="white",
                        justify="center"
                    )
                    e.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                    
                    e.insert(0, "-")
                    
                    self.grid_entries[(i, j)] = e
                    
                    e.bind("<KeyRelease>", lambda event, entry=e: self.check_cell_color(entry))

                    e.bind("<BackSpace>", lambda event, entry=e: self.force_on_delete(entry))
                    e.bind("<Delete>", lambda event, entry=e: self.force_on_delete(entry))

    def force_on_delete(self, entry):
        entry.after_idle(lambda: self._ensure_space(entry))

    def _ensure_space(self, entry):
        content = entry.get()
        if content == "":
            entry.insert(0, "-")

        self.check_cell_color(entry)

    def check_cell_color(self, entry):
        val = entry.get().strip().upper()
        if val[0] in ["1","2","3","4","5","6","7","8","9","C","F","J","D","E","I"]:
            if "K" in val:
                entry.config(fg="#03cffc")
            elif "P" in val:
                entry.config(fg="#fc03d3")
            elif "S" in val:
                entry.config(fg="#03fc45")
            elif "H" in val:
                entry.config(fg="#fc1703")
            elif "D" in val:
                entry.config(fg="#fcba03")
            else:
                entry.config(fg=self.fgcolor)

        else:
            entry.config(bg=self.bgcolor, fg=self.fgcolor)
        content = entry.get()

        if len(content)>1 and content[0]=="-":
            entry.delete(0, tk.END)
            entry.insert(0, content[1:])

    def get_data(self):
        if os.path.exists("data/theme.data"):
            with open("data/theme.data", "rb") as f:
                data = f.readlines()
                self.fgcolor = data[0].strip().decode() if isinstance(data[0], bytes) else data[0].strip()
                self.bgcolor = data[1].strip().decode() if isinstance(data[1], bytes) else data[1].strip()
                self.fontsize = int(data[2].strip())
                self.iconsize = int(data[3].strip())
                self.ingamesize = int(data[4].strip())
                self.dlsize = int(data[5].strip())

    def get_content(self):
        content = [["-" for _ in range(self.rows)] for __ in range(self.columns)]
        for i in range(self.rows):
            for j in range(self.columns):
                if not isinstance(self.grid_entries[(i, j)], tk.Text):
                    val = self.grid_entries[(i, j)].get()
                    content[i][j] = val
        return content


    def set_content(self, content_str):
        content = content_str.split("\n")
        print(content)
        for k in range(len(content)):
            content[k] = content[k].split("|")
        print(content)
        for i in range(self.rows):
            for j in range(self.columns):
                if i!=0 or j!=0:
                    self.grid_entries[(i,j)].delete(0, tk.END)
                    self.grid_entries[(i,j)].insert(0, content[i][j])