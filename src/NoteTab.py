import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil, zipfile
from datetime import datetime

class NoteTab:
    def __init__(self, notebook, title="Nouvelle feuille"):
        self.frame = ttk.Frame(notebook)

        self.img_checked = ImageTk.PhotoImage(file="assets/misc/checked.png")
        self.img_unchecked = ImageTk.PhotoImage(file="assets/misc/unchecked.png")

        self.fontsize = 12
        self.iconsize = 48
        self.ingamesize = 32
        self.dlsize = 48

        self.fgcolor = "#f7f7f7"
        self.bgcolor = "#1e1e1e"

        self.get_data()

        self.text = tk.Text(
            self.frame,
            wrap="word",
            undo=True,
            font=("Segoe UI", self.fontsize),
            bg=self.bgcolor,
            fg=self.fgcolor,
            insertbackground="white",
            relief="flat",
            padx=12,
            pady=12,
        )

        self.scrollbar = ttk.Scrollbar(self.frame, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        pil = Image.open("assets/icons/default.png")
        pil = pil.resize((self.iconsize, self.iconsize))
        self.tk_img = ImageTk.PhotoImage(pil)

        self.tag_counter = 0

        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<BackSpace>", self.on_backspace)

        self.filepath = None

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

    def on_key_release(self, event):
        self.replace_tags()
        self.replace_chara_tags()
        self.replace_markdown_tags()


    def replace_tags(self):

        for key, img_path in table_corres.items():

            tag_text = f"#{key}#"
            start = "1.0"

            while True:

                pos = self.text.search(tag_text, start, stopindex="end")

                if not pos:
                    break

                end = f"{pos}+{len(tag_text)}c"

                existing_tags = self.text.tag_names(pos)

                already_done = any(
                    t.startswith("hidden_")
                    for t in existing_tags
                )

                if not already_done:

                    pil = Image.open(f"assets/{img_path}")
                    if "ingame" in img_path:
                        pil = pil.resize((self.ingamesize, self.ingamesize))
                    else:
                        pil = pil.resize((self.iconsize, self.iconsize))

                    tk_img = ImageTk.PhotoImage(pil)

                    if not hasattr(self, "images"):
                        self.images = []

                    self.images.append(tk_img)

                    tag_name = f"hidden_{self.tag_counter}"
                    self.tag_counter += 1

                    self.text.tag_add(tag_name, pos, end)
                    self.text.tag_config(tag_name, elide=True)

                    self.text.image_create(pos, image=tk_img)

                start = end

    def on_backspace(self, event):

        insert_pos = self.text.index("insert")

        prev_pos = self.text.index(f"{insert_pos} -1c")

        tags = self.text.tag_names(prev_pos)

        hidden_tags = [t for t in tags if t.startswith("hidden_")]

        if hidden_tags:

            tag = hidden_tags[0]

            ranges = self.text.tag_ranges(tag)

            if ranges:

                start = ranges[0]
                end = ranges[1]

                self.text.delete(start, end)

                return "break"

    def replace_chara_tags(self):
        pattern = r"<[^=]+=[^>]+>"
        start = "1.0"

        while True:
            pos = self.text.search(pattern, start, stopindex="end", regexp=True)

            if not pos:
                break

            chunk = self.text.get(pos, f"{pos}+100c")
            match = re.match(r"<([^=]+)=([^>]+)>", chunk)

            if not match:
                start = f"{pos}+1c"
                continue

            full_tag = match.group(0)
            A = match.group(1)
            B = match.group(2)

            end = f"{pos}+{len(full_tag)}c"
            existing_tags = self.text.tag_names(pos)

            already_done = any(
                t.startswith("hidden_")
                for t in existing_tags
            )

            if not already_done:
                cus_query = f"{A}_{B}.png"
                img_path = f"assets/downloaded_data/{cus_query.replace("/", "")}"
                if not os.path.exists(img_path):
                    chara = get_chara_from_str(A)
                    get_move_img_from_data(A, *get_move_data(chara, B))     

                pil = Image.open(img_path)
                pil = pil.resize((self.dlsize, self.dlsize))

                tk_img = ImageTk.PhotoImage(pil)

                if not hasattr(self, "images"):
                    self.images = []

                self.images.append(tk_img)

                tag_name = f"hidden_{self.tag_counter}"
                self.tag_counter += 1

                self.text.tag_add(tag_name, pos, end)
                self.text.tag_config(tag_name, elide=True)

                self.text.image_create(pos, image=tk_img)

            start = end

    def toggle_cb(self, event, lbl):
        is_checked = self.cbs[lbl]
        if is_checked:
            lbl.config(image=self.img_unchecked)
            is_checked = False
        else:
            lbl.config(image=self.img_checked)
            is_checked = True
        self.cbs[lbl] = is_checked
        print(self.cbs[lbl])


    def replace_markdown_tags(self):
        pattern = r"\[CB\]"
        start = "1.0"

        if not hasattr(self, "cb_counter"):
            self.cb_counter = 0
        if not hasattr(self, "cbs"):
            self.cbs = dict()

        while True:
            # Recherche du pattern avec RegEx
            pos = self.text.search(pattern, start, stopindex="end", regexp=True)

            if not pos:
                break  # Plus de balises trouvées, on arrête
            
            # Le texte recherché fait exactement 4 caractères : "[CB]"
            tag_length = 4
            end = f"{pos}+{tag_length}c"

            # Vérification si la balise a déjà été traitée
            existing_tags = self.text.tag_names(pos)
            already_done = any(t.startswith("hidden_") for t in existing_tags)

            if not already_done:
                cb_label = tk.Label(self.text, image=self.img_unchecked, bg=self.bgcolor, cursor="hand2")
                
                is_checked = False
                self.cbs[cb_label] = is_checked


                cb_label.bind("<Button-1>", lambda event, lbl=cb_label: self.toggle_cb(event, lbl))

                # Stockage si tu as besoin de l'état global plus tard
                

                tag_name = f"hidden_{self.cb_counter}"
                self.cb_counter += 1
                
                self.text.tag_add(tag_name, pos, end)
                self.text.tag_config(tag_name, elide=True)

                # Insertion du Label customisé à la place du texte
                self.text.window_create(pos, window=cb_label)

            # On avance le curseur de recherche APRÈS le tag actuel pour éviter la boucle infinie
            start = end
            
    def check_boxes(self):
        print(self.cbs)
        if not self.cbs or len(self.cbs)<1:
            return
        for k,v in self.cbs.items():
            if v:
                k.config(image=self.img_checked)
            else:
                k.config(image=self.img_unchecked)