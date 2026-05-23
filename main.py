import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil
from fetchdata import get_chara_from_str, get_move_data, get_move_img_from_data

putain_de_bt = {
    "624" : "63214",
    "426" : "41236",
    "684" : "69874",
    "486" : "47896",
    "248" : "21478",
    "842" : "87412",
    "268" : "23698",
    "862" : "89632",
}

charas = [
    " ",
    "ABA", 
    "Anji",
    "Asuka",
    "Axl",
    "Baiken",
    "Bedman",
    "Bridget",
    "Chaos",
    "Chipp",
    "Dizzy",
    "Elphelt",
    "Faust",
    "Giovanna",
    "Goldlewis",
    "I-No",
    "Jack-O'",
    "Jam",
    "Johnny",
    "Ky",
    "Lucy",
    "May",
    "Millia",
    "Nagoriyuki",
    "Potemkin",
    "Ramlethal",
    "Sin",
    "Slayer",
    "Sol",
    "Testament",
    "Unika",
    "Venom",
    "Zato"
]

table_corres = {
    "Asya" : "icons/default.png",
    "236" : "ingame/236.png",
    "214" : "ingame/214.png",
    "623" : "ingame/623.png",
    "421" : "ingame/421.png",
}

for c in charas:
    if c.strip():
        table_corres[c] = f"icons/{c}.jpg"

for i in range(1,10):
    table_corres[f"{i}"] = f"ingame/{i}.png"

for k in ["P", "K", "S", "H", "D"]:
    table_corres[k] = f"ingame/{k}.png"

for bt in putain_de_bt.keys():
    table_corres[bt] = f"ingame/{bt}.png"

class NoteTab:
    def __init__(self, notebook, title="Nouvelle feuille"):
        self.frame = ttk.Frame(notebook)

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

        # détection frappe clavier
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
        self.replace_custom_tags()


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

                    # charger image
                    pil = Image.open(f"assets/{img_path}")
                    if "ingame" in img_path:
                        pil = pil.resize((self.ingamesize, self.ingamesize))
                    else:
                        pil = pil.resize((self.iconsize, self.iconsize))

                    tk_img = ImageTk.PhotoImage(pil)

                    # IMPORTANT :
                    # stocker référence sinon Tkinter détruit l'image
                    if not hasattr(self, "images"):
                        self.images = []

                    self.images.append(tk_img)

                    # cacher texte
                    tag_name = f"hidden_{self.tag_counter}"
                    self.tag_counter += 1

                    self.text.tag_add(tag_name, pos, end)
                    self.text.tag_config(tag_name, elide=True)

                    # afficher image
                    self.text.image_create(pos, image=tk_img)

                start = end

    def on_backspace(self, event):

        # position actuelle du curseur
        insert_pos = self.text.index("insert")

        # position précédente
        prev_pos = self.text.index(f"{insert_pos} -1c")

        # récupérer les tags à cette position
        tags = self.text.tag_names(prev_pos)

        hidden_tags = [t for t in tags if t.startswith("hidden_")]

        if hidden_tags:

            tag = hidden_tags[0]

            # récupérer plage du tag
            ranges = self.text.tag_ranges(tag)

            if ranges:

                start = ranges[0]
                end = ranges[1]

                # supprimer image + texte caché
                self.text.delete(start, end)

                return "break"

    def replace_custom_tags(self):
            # Pattern adapté pour la recherche native Tkinter (sans les groupes de capture complexes au milieu)
            # Tkinter search a besoin d'un pattern simple, on extrait les variables après.
            pattern = r"<[^=]+=[^>]+>"
            start = "1.0"

            while True:
                # On cherche directement via Tkinter en mode regexp
                pos = self.text.search(pattern, start, stopindex="end", regexp=True)

                if not pos:
                    break  # Plus aucune balise trouvée, on s'arrête

                # On récupère le texte exact trouvé à cette position pour en extraire A et B
                # On regarde un peu plus loin (par exemple 100 caractères) pour capturer toute la balise
                chunk = self.text.get(pos, f"{pos}+100c")
                match = re.match(r"<([^=]+)=([^>]+)>", chunk)

                if not match:
                    # Sécurité au cas où la recherche Tkinter et re ne s'entendent pas
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

                # On avance le pointeur juste après la balise qu'on vient de traiter
                start = end

    def asya(self, image):
        i = len(self.asyas)
        image = Image.open(image).resize((self.iconsize, self.iconsize))
        self.img = ImageTk.PhotoImage(image)
        self.asyas.append(ImageTk.PhotoImage(image))
        self.img_label = tk.Label(self.text, image=self.asyas[i])
        self.text.window_create(
            tk.END,
            window=self.img_label
        )

class SheetTab:
    
    def __init__(self, parent, rows, columns):
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

        self.window.title("Table")
        #self.window.geometry("400x500")
        self.window.configure(bg=self.bgcolor)

        self.build_ui(rows, columns)

    def build_ui(self, rows, columns):
        for i in range(rows):
            for j in range(columns):
                
                self.e = tk.Entry(self.window, width=20, fg=self.fgcolor, bg=self.bgcolor,
                               font=('Arial',self.fontsize,'bold'))
                
                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, "")

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

        self.get_data()

        self.window.title("Profil utilisateur")
        self.window.geometry("400x500")
        self.window.configure(bg=self.bgcolor)


        self.opt = tk.StringVar(value="")

        self.pseudo = None
        self.perso = None
        self.perso_img = None
        
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

        # ===== TITRE =====
        title = tk.Label(
            self.window,
            text="Profil",
            font=("Segoe UI", self.fontsize, "bold"),
            bg=self.bgcolor,
            fg=self.fgcolor
        )
        title.pack(pady=20)

        # ===== PSEUDO =====
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

        # ===== MAIN =====
        
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
            os.makedirs(f"profiles/{self.pseudo}/{self.perso}/charas")
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


class CustomizationWindow:
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

        # ===== TITRE =====
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

class SelectChara:
    def __init__(self, parent, data):
        self.window = tk.Toplevel(parent)
        self.window.transient(parent)
        self.window.grab_set()

        self.fontsize = 12
        self.iconsize = 48
        self.ingamesize = 32
        self.dlsize = 48

        self.bgcolor = "#f7f7f7"
        self.bgcolor = "#1e1e1e"

        self.get_data()

        self.window.title("Note de counterplay")
        self.window.geometry("450x500")
        self.window.configure(bg=self.bgcolor)

        self.photos = []

        self.pseudo = data[0]
        self.perso = data[1]
        self.perso_img = data[2]

        self.adversaire = None
        self.adversaire_img = None
        
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
        i=0
        j=0
        for file in os.listdir("assets/icons"):
            if ".jpg" in file:
                img = Image.open(f"assets/icons/{file}")
                img = img.resize((self.iconsize, self.iconsize))
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
        if not os.path.exists(f"profiles/{self.pseudo}/{self.perso}/counterplay/{self.adversaire}.caca"):   
            with open(f"profiles/{self.pseudo}/{self.perso}/counterplay/{self.adversaire}.caca","w") as f:
                f.write(f"COUNTERPLAY CONTRE #{self.adversaire}# AS #{self.perso}# :\n")
                f.close()
        self.window.destroy()

        


class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrysanthème")
        self.root.geometry("1100x700")

        self.fontsize = 12
        self.iconsize = 48
        self.ingamesize = 32
        self.dlsize = 48

        self.bgcolor = "#f7f7f7"
        self.bgcolor = "#1e1e1e"

        self.pseudo = None
        self.perso = None
        self.perso_img = "default.png"
        self.asyapic = "assets/icons/default.png"

        self.get_data()

        self.root.configure(bg=self.bgcolor)

        self.profile_btn = None

        self.setup_style()
        self.create_toolbar()
        self.create_notebook()
        self.create_statusbar()

        self.new_tab()

        self.root.bind("<Control-n>", lambda e: self.new_tab())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-w>", lambda e: self.close_current_tab())
        self.root.bind("<Double-1>", lambda e: self.close_tab_on_double_click())
        self.root.bind("<<PROFILE_UPDATED>>", lambda e: self.update_toolbar())
        self.root.bind("<<THEME_UPDATED>>", lambda e:self.root.destroy())

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

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TNotebook",
            background="#121212",
            borderwidth=0,
        )

        style.configure(
            "TNotebook.Tab",
            background="#2a2a2a",
            foreground="white",
            padding=(18, 10),
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", "#4f46e5")],
            foreground=[("selected", "white")],
        )

        style.configure(
            "Toolbar.TFrame",
            background="#181818",
        )

        style.configure(
            "Toolbar.TButton",
            background="#2a2a2a",
            foreground="white",
            padding=6,
        )

        self.root.option_add('*tearOff', False)

    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.root, style="Toolbar.TFrame")
        self.toolbar.pack(fill="x")

        self.build_toolbar_buttons()

    def build_toolbar_buttons(self):

        self.icons = {
            "profile": ImageTk.PhotoImage(
                Image.open(self.perso_img).resize((20, 20))
            ),
        }

        buttons = [
            (None, "➕ Note basique", self.new_tab),
            (None, "🚩 Note de counterplay", self.new_counterplay),
            (None, "🚥 Table de roundstart", self.new_roundstart),
            (None, "💾 Sauvegarder", self.save_file),
            (None, "📂 Ouvrir", self.open_file),
            (None, "Customisation", self.customize),
        ]

        # reset frame (important)
        for widget in self.toolbar.winfo_children():
            widget.destroy()

        # bouton profil (IMPORTANT)
        profile_text = self.pseudo if self.pseudo else "Ton profil"

        self.profile_btn = ttk.Button(
            self.toolbar,
            text=profile_text,
            image=self.icons["profile"],
            compound="left",
            command=self.profile,
            style="Toolbar.TButton",
        )

        self.profile_btn.pack(side="left", padx=6, pady=6)

        # boutons classiques
        for icon, text, command in buttons:
            btn = ttk.Button(
                self.toolbar,
                text=text,
                command=command,
                style="Toolbar.TButton",
            )
            btn.pack(side="left", padx=6, pady=6)


    def update_toolbar(self):
        self.get_data()
        self.build_toolbar_buttons()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tabs = []

        self.notebook.bind("<<NotebookTabChanged>>", self.update_status)

    def create_statusbar(self):
        self.status = tk.StringVar(value="Prêt")

        statusbar = tk.Label(
            self.root,
            textvariable=self.status,
            anchor="w",
            bg="#181818",
            fg="#cccccc",
            padx=10,
            pady=5,
        )

        statusbar.pack(fill="x", side="bottom")

    def get_current_tab(self):
        current = self.notebook.index("current")
        return self.tabs[current]

    def new_tab(self, title="Nouvelle feuille"):
        tab = NoteTab(self.notebook, title)
        self.tabs.append(tab)

        self.notebook.add(tab.frame, text=title)

        self.notebook.select(tab.frame)
        tab.text.focus_set()

        self.status.set(f"Nouvelle feuille créée : {title}")



    def new_counterplay(self):
        sel = SelectChara(self.root, (self.pseudo, self.perso, self.perso_img))
        self.root.wait_window(sel.window)
        char = sel.adversaire
        path = Path(f"profiles/{self.pseudo}/{self.perso}/counterplay/{char}.caca")

        try:
            content = path.read_text(encoding="utf-8")

            self.new_tab(path.name)

            tab = self.get_current_tab()
            tab.text.insert("1.0", content)
            tab.filepath = path
            tab.replace_tags()
            tab.replace_custom_tags()

            self.status.set(f"Ouvert : {path.name}")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def new_roundstart(self):
        sel = SelectChara(self.root, (self.pseudo, self.perso, self.perso_img))
        self.root.wait_window(sel.window)
        char = sel.adversaire
        path = Path(f"profiles/{self.pseudo}/{self.perso}/roundstart/{char}.pipi")
        sh = SheetTab(self.root, 5, 5)

    def close_tab_on_double_click(self):
        if len(self.tabs) == 1:
            messagebox.showwarning(
                "Action impossible",
                "Il doit rester au moins une feuille ouverte.",
            )
            return

        current_index = self.notebook.index("current")

        self.notebook.forget(current_index)
        self.tabs.pop(current_index)

        self.status.set("Feuille fermée")

    def save_file(self):
        tab = self.get_current_tab()

        if not tab.filepath:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".caca",
                initialdir=f"profiles/{self.pseudo}/{self.perso}",
                filetypes=[
                    ("Fichier trop cool", "*.caca"),
                    ("Fichier texte", "*.txt"),
                    ("Markdown", "*.md"),
                    ("Tous les fichiers", "*.*"),
                ],
            )

            if not filepath:
                return

            tab.filepath = Path(filepath)

        content = tab.text.get("1.0", "end-1c")

        try:
            tab.filepath.write_text(content, encoding="utf-8")

            filename = tab.filepath.name
            current = self.notebook.index("current")
            self.notebook.tab(current, text=filename)

            self.status.set(f"Sauvegardé : {filename}")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def open_file(self):
        filepath = filedialog.askopenfilename(
            initialdir=f"profiles/{self.pseudo}/{self.perso}",
            filetypes=[
                ("Fichier trop cool", "*.caca"),
                ("Fichier texte", "*.txt"),
                ("Markdown", "*.md"),
                ("Tous les fichiers", "*.*"),
            ]
        )

        if not filepath:
            return

        path = Path(filepath)

        try:
            content = path.read_text(encoding="utf-8")

            self.new_tab(path.name)

            tab = self.get_current_tab()
            tab.text.insert("1.0", content)
            tab.filepath = path
            tab.replace_tags()
            tab.replace_custom_tags()

            self.status.set(f"Ouvert : {path.name}")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def profile(self):
        def after_close():
            self.update_toolbar()

        ProfileWindow(self.root)
        self.root.after(500, self.update_toolbar)

    def customize(self):
        CustomizationWindow(self.root)

    def update_status(self, event=None):
        try:
            tab = self.get_current_tab()
            title = self.notebook.tab("current", "text")
            chars = len(tab.text.get("1.0", "end-1c"))

            self.status.set(f"Feuille active : {title} | {chars} caractères")
        except:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
