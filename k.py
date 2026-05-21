import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

TAG_TEXT = "#image#"


class InlineImageText:
    def __init__(self, root):
        self.root = root

        self.text = tk.Text(root, wrap="word", undo=True, font=("Arial", 14))
        self.text.pack(fill="both", expand=True)

        # Charger l'image
        pil = Image.open("assets/icons/default.png")
        pil = pil.resize((48,48))
        self.tk_img = ImageTk.PhotoImage(pil)

        # compteur unique pour les tags
        self.tag_counter = 0

        # détection frappe clavier
        self.text.bind("<KeyRelease>", self.on_key_release)

        # Barre de boutons
        toolbar = tk.Frame(root)
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Importer", command=self.import_file).pack(side="left")
        tk.Button(toolbar, text="Sauvegarder", command=self.save).pack(side="left")

        self.text.bind("<BackSpace>", self.on_backspace)

    def on_key_release(self, event):
        self.replace_tags()

    def replace_tags(self):
        """
        Cherche toutes les occurrences visibles de #image#
        et les remplace visuellement par une image.
        """

        start = "1.0"

        while True:
            pos = self.text.search(TAG_TEXT, start, stopindex="end")

            if not pos:
                break

            end = f"{pos}+{len(TAG_TEXT)}c"

            # Vérifie si déjà remplacé
            existing_tags = self.text.tag_names(pos)

            already_done = any(t.startswith("hidden_") for t in existing_tags)

            if not already_done:

                # cacher le texte
                tag_name = f"hidden_{self.tag_counter}"
                self.tag_counter += 1

                self.text.tag_add(tag_name, pos, end)
                self.text.tag_config(tag_name, elide=True)

                # insérer image AVANT le texte caché
                self.text.image_create(pos, image=self.tk_img)

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

    def import_file(self):
        """
        Importe un fichier texte.
        Les #image# sont automatiquement convertis visuellement.
        """

        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("Tous les fichiers", "*.*")]
        )

        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)

        # refaire les images
        self.replace_tags()

    def save(self):
        content = self.text.get("1.0", "end-1c")

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )

        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            print("Contenu sauvegardé :")
            print(content)


root = tk.Tk()
root.title("Text avec images inline")

app = InlineImageText(root)

root.mainloop()