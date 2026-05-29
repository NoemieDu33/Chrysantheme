import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil, zipfile
from datetime import datetime

from src.NoteTab import NoteTab
from src.ProfileWindow import ProfileWindow
from src.SelectChara import SelectChara
from src.SheetTab import SheetTab
from src.CustomizationWindow import CustomizationWindow

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrysanthème")
        self.root.geometry("1300x800")

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
        if self.perso_img=="default.png":
            self.perso_img = "assets/icons/default.png"
        self.icons = {
            "profile": ImageTk.PhotoImage(
                Image.open(f"{self.perso_img}").resize((20, 20))
            ),
        }

        buttons = [
            (None, "➕ Note basique", self.new_tab),
            (None, "🚩 Note de counterplay", self.new_counterplay),
            (None, "🚥 Table de roundstart", self.new_roundstart),
            (None, "🏅 Objectifs", self.show_goals),
        ]

        for widget in self.toolbar.winfo_children():
            widget.destroy()

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

        for icon, text, command in buttons:
            btn = ttk.Button(
                self.toolbar,
                text=text,
                command=command,
                style="Toolbar.TButton",
            )
            btn.pack(side="left", padx=6, pady=6)

        self.file_menu = tk.Menu(self.root, tearoff=0, font=("Segoe UI", self.fontsize))
        self.file_menu.add_command(label="💾 Sauvegarder", command=self.save_file)
        self.file_menu.add_command(label="📂 Ouvrir", command=self.open_file)
        self.file_menu.add_command(label="❌ Fermer", command=self.close_tab_on_double_click)

        self.file_btn = ttk.Button(
            self.toolbar,
            text="Fichier",
            command=self.show_file_menu,
            style="Toolbar.TButton",
        )
        self.file_btn.pack(side="left", padx=6, pady=6)

        self.settings_menu = tk.Menu(self.root, tearoff=0, font=("Segoe UI", self.fontsize))
        self.settings_menu.add_command(label="🖌️ Customisation", command=self.customize)
        self.settings_menu.add_command(label="Importer", command=self.import_data)
        self.settings_menu.add_command(label="Exporter", command=self.export_data)

        self.settings_btn = ttk.Button(
            self.toolbar,
            text="⚙️ Paramètres",
            command=self.show_settings_menu,
            style="Toolbar.TButton",
        )
        self.settings_btn.pack(side="left", padx=6, pady=6)

    def show_goals(self):
        if self.pseudo is not None:
            filepath = f"profiles/{self.pseudo}/{self.perso}/uniques/objectifs.caca"
            if not os.path.exists(filepath):
                with open(filepath, "w") as f:
                    f.write(f"Objectifs pour {self.pseudo} <{self.perso}=c.S>\n")
                    f.close()
            path = Path(filepath)

            content = path.read_text(encoding="utf-8")
            cbsglob = None
            if "!-/" in content:
                cbsglob = content.split("!-/")[1][:-3]
                content = content.split("!-/")[0]

            i=0
            tab = NoteTab(self.notebook, path.name)
            self.tabs.append(tab)
            self.notebook.add(tab.frame, text=path.name)
            tab.text.insert("1.0", content)
            tab.replace_tags()
            tab.replace_chara_tags()
            tab.replace_markdown_tags()
            if cbsglob is not None and len(cbsglob):
                i=0
                for k,v in tab.cbs.items():
                    tab.cbs[k] = int(cbsglob[i])
                    i+=1

            self.notebook.select(tab.frame)
            tab.filepath = path
            self.status.set(f"Ouvert : {path.name}")
            tab.check_boxes()


        else:
            messagebox.showerror("Erreur", "Tu n'as pas setup de profil!")   
            return


    def show_file_menu(self):
        x = self.file_btn.winfo_rootx()
        y = self.file_btn.winfo_rooty() + self.file_btn.winfo_height()
        self.file_menu.post(x, y)
        self.root.bind("<Button-1>", self.close_file_menu, add="+")

    def show_settings_menu(self):
        x = self.settings_btn.winfo_rootx()
        y = self.settings_btn.winfo_rooty() + self.settings_btn.winfo_height()
        self.settings_menu.post(x, y)
        self.root.bind("<Button-1>", self.close_settings_menu, add="+")

    def close_file_menu(self, event=None):
        self.root.unbind("<Button-1>")
        self.file_menu.unpost()
        self.file_menu.grab_release()

    def close_settings_menu(self, event=None):
        self.root.unbind("<Button-1>")
        self.settings_menu.unpost()
        self.settings_menu.grab_release()

    def import_data(self):
        filepath = filedialog.askopenfilename(
            initialdir=f".",
            filetypes=[
                ("Archive", "*.zip"),
            ]
        )

        if not filepath:
            return

        path = Path(filepath)

        with zipfile.ZipFile(path, 'r') as zObject:
            zObject.extractall(path=".")
            
        messagebox.showinfo(
            "Import",
            "Données importées!"
        )

    def export_data(self):
        shutil.make_archive(base_name=f"export/{self.pseudo}_{str(datetime.now())[:19].replace(" ","_").replace(":","_")}", 
                            format='zip', 
                            root_dir=".",
                            base_dir=f"profiles/{self.pseudo}/",
                            )

        messagebox.showinfo(
            "Export",
            "Données exportées en .zip!"
        )


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
        if sel.adversaire is None:
            return
        path = Path(f"profiles/{self.pseudo}/{self.perso}/counterplay/{char}.caca")
        if not os.path.exists(path):   
            with open(path,"w") as f:
                f.write(f"COUNTERPLAY CONTRE #{char}# AS #{self.perso}# :\n")
                f.close()
        try:
            content = path.read_text(encoding="utf-8")

            self.new_tab(path.name)

            tab = self.get_current_tab()
            tab.text.insert("1.0", content)
            tab.filepath = path
            tab.replace_tags()
            tab.replace_chara_tags()
            tab.replace_markdown_tags()

            self.status.set(f"Ouvert : {path.name}")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def new_roundstart(self):
        sel = SelectChara(self.root, (self.pseudo, self.perso, self.perso_img))
        self.root.wait_window(sel.window)
        char = sel.adversaire
        
        if not char:
            return

        path = Path(f"profiles/{self.pseudo}/{self.perso}/roundstart/{char}.pipi")
        
        tab = SheetTab(self.notebook, title=f"{char}.pipi", 
            rows=8, columns=8,
            chara_1 = self.perso, chara_2 = sel.adversaire
        )
        self.tabs.append(tab)
        self.notebook.add(tab.frame, text=f"{char}.pipi")
        self.notebook.select(tab.frame)
        
        tab.filepath = path
        
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                tab.set_content(content)
            except Exception as e:
                messagebox.showerror("Erreur de lecture", str(e))

        self.status.set(f"Table Roundstart créée pour {char}")

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
        is_sheet = isinstance(tab, SheetTab)

        if not tab.filepath:

            default_ext = ".pipi" if is_sheet else ".caca"
            file_types = [("Fichier Roundstart", "*.pipi")] if is_sheet else [("Fichier note", "*.caca")]
            file_types.extend([("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")])

            filepath = filedialog.asksaveasfilename(
                defaultextension=default_ext,
                initialdir=f"profiles/{self.pseudo}/{self.perso}",
                filetypes=file_types,
            )

            if not filepath:
                return

            tab.filepath = Path(filepath)

        if is_sheet:
            c = tab.get_content()
            content = ""
            for l in c:
                content+=f"{'|'.join(l)}\n"

            
        else:
            tab.replace_tags()
            tab.replace_chara_tags()
            tab.replace_markdown_tags()
            content = tab.text.get("1.0", "end-1c")
            if tab.cbs is not None and len(tab.cbs)>0:
                content += "\n!-/"
                for cb, state in tab.cbs.items():
                    content += "1" if state else "0"
                content += "/-!"
                    

        try:
            
            tab.filepath.write_text(content, encoding="utf-8")

            filename = tab.filepath.name
            current = self.notebook.index("current")
            self.notebook.tab(current, text=filename)

            self.status.set(f"Sauvegardé : {filename}")
            print("save fini")

        except Exception as e:
            print("err")
            messagebox.showerror("Erreur", str(e))

    def open_file(self):
        filepath = filedialog.askopenfilename(
            initialdir=f"profiles/{self.pseudo}/{self.perso}",
            filetypes=[
                ("Tous les fichiers de notes", "*.caca *.pipi"),
                ("Fichier trop cool", "*.caca"),
                ("Fichier Roundstart", "*.pipi"),
                ("Tous les fichiers", "*.*"),
            ]
        )

        if not filepath:
            return

        path = Path(filepath)

        try:
            content = path.read_text(encoding="utf-8")

            if path.suffix == ".pipi":
                tab = SheetTab(self.notebook, title=path.name)
                self.tabs.append(tab)
                self.notebook.add(tab.frame, text=path.name)
                tab.set_content(content)
            else:
                cbsglob = None
                if "!-/" in content:
                    cbsglob = content.split("!-/")[1][:-3].split("")
                    content = content.split("!-/")[0]

                tab = NoteTab(self.notebook, path.name)
                self.tabs.append(tab)
                self.notebook.add(tab.frame, text=path.name)
                tab.text.insert("1.0", content)
                tab.replace_tags()
                tab.replace_chara_tags()
                tab.replace_markdown_tags()
                if cbsglob is not None and len(cbsglob):
                    i=0
                    for k,v in tab.cbs.items():
                        tab.cbs[k] = int(cbsglob[i])
                        i+=1

            self.notebook.select(tab.frame)
            tab.filepath = path
            self.status.set(f"Ouvert : {path.name}")
            tab.check_boxes()

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
        tab = self.get_current_tab()
        title = self.notebook.tab("current", "text")
        
        if isinstance(tab, SheetTab):
            self.status.set(f"Table active : {title} | Grille {tab.rows}x{tab.columns}")
        else:
            chars = len(tab.text.get("1.0", "end-1c"))
            self.status.set(f"Feuille active : {title} | {chars} caractères")
