import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os
import shutil
import re


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
    table_corres[c] = f"icons/{c}.jpg"

for i in range(1,10):
    table_corres[f"{i}"] = f"ingame/{i}.png"

for k in ["P", "K", "S", "H", "D"]:
    table_corres[k] = f"ingame/{k}.png"

for bt in putain_de_bt.keys():
    table_corres[bt] = f"ingame/{bt}.png"

def balise_reader(self, balise):
    txt = balise.strip("#").strip()
    if balise[0] in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        numbers = balise[:-1]
        letter = balise[-1]
        img_numbers = table_corres[numbers]
        img_letter = table_corres[letter]
        return (img_numbers, img_letter)
    else:
        if balise in table_corres.keys():
            return (table_corres[balise], None)



class NoteTab:
    def __init__(self, notebook, title="Nouvelle note"):
        self.frame = ttk.Frame(notebook)
        self.text = tk.Text(
            self.frame,
            wrap="word",
            undo=True,
            font=("Segoe UI", 11),
            bg="#1e1e1e",
            fg="#f5f5f5",
            insertbackground="white",
            relief="flat",
            padx=12,
            pady=12,
        )

        self.scrollbar = ttk.Scrollbar(self.frame, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
    
        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.asyas = []

        notebook.add(self.frame, text=title)

        self.filepath = None
        self.text.bind("<<Modified>>", self.on_text_change)

    def on_text_change(self, event):

        # éviter boucle infinie
        if getattr(self, "_processing", False):
            return

        self._processing = True

        contenu = self.text.get("1.0", "end-1c")

        # détecte #balise#
        matches = list(re.finditer(r"#(.*?)#", contenu))

        for match in reversed(matches):

            balise_complete = match.group(0)   # ex: #Asya#
            balise = match.group(1)            # ex: Asya

            if balise in table_corres:

                # position début/fin
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"

                # supprime texte
                self.text.delete(start, end)

                # insère image
                self.insert_image(start, table_corres[balise])

        self.text.edit_modified(False)
        self._processing = False


        # éviter boucle infinie
        if getattr(self, "_processing", False):
            return

        self._processing = True

        contenu = self.text.get("1.0", "end-1c")

        # détecte #balise#
        matches = list(re.finditer(r"#(.*?)#", contenu))

        for match in reversed(matches):

            balise_complete = match.group(0)   # ex: #Asya#
            balise = match.group(1)            # ex: Asya

            if balise in table_corres:

                # position début/fin
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"

                # supprime texte
                self.text.delete(start, end)

                # insère image
                self.insert_image(start, table_corres[balise])

        self.text.edit_modified(False)
        self._processing = False



    def insert_image(self, index, image_path):

        image = Image.open(f"assets/{image_path}")
        image = image.resize((32, 32))

        photo = ImageTk.PhotoImage(image)

        # IMPORTANT : garder référence
        self.asyas.append(photo)

        label = tk.Label(
            self.text,
            image=photo,
            bg="#1e1e1e",
            bd=0
        )

        self.text.window_create(index, window=label)

    
    def asya(self, image):
        i = len(self.asyas)
        image = Image.open(image).resize((48, 48))
        self.img = ImageTk.PhotoImage(image)
        self.asyas.append(ImageTk.PhotoImage(image))
        self.img_label = tk.Label(self.text, image=self.asyas[i])
        self.text.window_create(
            tk.END,
            window=self.img_label
        )

class ProfileWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.transient(parent)
        self.window.grab_set()

        self.window.title("Profil utilisateur")
        self.window.geometry("400x500")
        self.window.configure(bg="#1e1e1e")


        self.opt = tk.StringVar(value="")

        

        self.pseudo = None
        self.perso = None
        self.perso_img = None
        

        self.get_data()
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
                print(self.perso_img)

    def build_ui(self):

        # ===== TITRE =====
        title = tk.Label(
            self.window,
            text="Profil",
            font=("Segoe UI", 18, "bold"),
            bg="#1e1e1e",
            fg="white"
        )
        title.pack(pady=20)

        # ===== PSEUDO =====
        pseudo_label = tk.Label(
            self.window,
            text="Pseudo :",
            bg="#1e1e1e",
            fg="white"
        )
        pseudo_label.pack(fill="x", anchor="w", padx=30)

        self.pseudo_entry = tk.Entry(
            self.window,
            font=("Segoe UI", 12),
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
            font=("Segoe UI", 12),
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

        print(f"Pseudo :{self.pseudo}\nMain: {self.perso}")
        if not os.path.exists(self.pseudo):
            os.makedirs(f"{self.pseudo}")
        if not os.path.exists(f"{self.pseudo}/{self.perso}"):
            os.makedirs(f"{self.pseudo}/{self.perso}")
            os.makedirs(f"{self.pseudo}/{self.perso}/roundstart")
            os.makedirs(f"{self.pseudo}/{self.perso}/counterplay")
            os.makedirs(f"{self.pseudo}/{self.perso}/charas")
            os.makedirs(f"{self.pseudo}/{self.perso}/random")
        with open("data/profile.data","wb") as f:
            f.write(f"{self.pseudo}\n{self.perso}".encode())
            f.close()        

        messagebox.showinfo(
            "Profil",
            "Profil sauvegardé !"
        )

        self.window.destroy()
        self.window.master.event_generate("<<PROFILE_UPDATED>>")



class SelectChara:
    def __init__(self, parent, data):
        self.window = tk.Toplevel(parent)
        self.window.transient(parent)
        self.window.grab_set()

        self.window.title("Note de counterplay")
        self.window.geometry("450x500")
        self.window.configure(bg="#1e1e1e")

        self.photos = []

        self.pseudo = data[0]
        self.perso = data[1]
        self.perso_img = data[2]

        self.adversaire = None
        self.adversaire_img = None
        
        self.build_ui()

    def build_ui(self):

        # title = tk.Label(
        #     self.window,
        #     text="Counterplay contre qui?",
        #     font=("Segoe UI", 18, "bold"),
        #     bg="#1e1e1e",
        #     fg="white"
        # )
        # title.grid(column=0, row=0)

        i=0
        j=0
        for file in os.listdir("assets/icons"):
            if ".jpg" in file:
                img = Image.open(f"assets/icons/{file}")
                img = img.resize((64,64))
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
        if not os.path.exists(f"{self.pseudo}/{self.perso}/counterplay/{self.adversaire}.caca"):   
            with open(f"{self.pseudo}/{self.perso}/counterplay/{self.adversaire}.caca","w") as f:
                f.write(f"COUNTERPLAY CONTRE {self.adversaire} AS {self.perso}:\n")
                f.close()
        self.window.destroy()

        


class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrysanthème")
        self.root.geometry("1100x700")
        self.root.configure(bg="#121212")

        self.pseudo = None
        self.perso = None
        self.perso_img = "default.png"
        self.asyapic = "assets/icons/default.png"

        self.profile_btn = None

        self.get_data()

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
                print(self.perso_img)

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

    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.root, style="Toolbar.TFrame")
        self.toolbar.pack(fill="x")

        self.build_toolbar_buttons()

    def build_toolbar_buttons(self):

        self.icons = {
            "profile": ImageTk.PhotoImage(
                Image.open(self.perso_img).resize((20, 20))
            ),
            "asya": ImageTk.PhotoImage(
                Image.open(self.asyapic).resize((20,20))
            ),
        }

        buttons = [
            (None, "➕ Note basique", self.new_tab),
            (None, "🚩 Note de counterplay", self.new_counterplay),
            (None, "🚥 Table de roundstart", self.new_roundstart),
            (None, "💾 Sauvegarder", self.save_file),
            (None, "📂 Ouvrir", self.open_file),
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

        self.asya_btn = ttk.Button(
            self.toolbar,
            text="Asya",
            image=self.icons["asya"],
            compound="left",
            command=self.asya,
            style="Toolbar.TButton",
        )

        self.asya_btn.pack(side="left", padx=6, pady=6)


    def asya(self):
        print("cc")
        cur = self.get_current_tab()
        cur.asya()

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

        self.notebook.select(tab.frame)
        tab.text.focus_set()

        self.status.set(f"Nouvelle feuille créée : {title}")



    def new_counterplay(self):

        sel = SelectChara(self.root, (self.pseudo, self.perso, self.perso_img))
        self.root.wait_window(sel.window)
        char = sel.adversaire
        path = Path(f"{self.pseudo}/{self.perso}/counterplay/{char}.caca")

        try:
            content = path.read_text(encoding="utf-8")

            self.new_tab(path.name)

            tab = self.get_current_tab()
            tab.text.insert("1.0", content)
            tab.filepath = path

            self.status.set(f"Ouvert : {path.name}")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def new_roundstart(self):
        pass

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
                initialdir=self.perso,
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
            initialdir=self.perso,
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

            self.status.set(f"Ouvert : {path.name}")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def profile(self):
        def after_close():
            self.update_toolbar()

        ProfileWindow(self.root)
        self.root.after(500, self.update_toolbar)

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
