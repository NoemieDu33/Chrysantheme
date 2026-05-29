import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil, zipfile
from datetime import datetime

from fetchdata import get_chara_from_str, get_move_data, get_move_img_from_data

from NotesApp import NotesApp



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

for k in ["P", "K", "S", "H", "D", "FD", "RC"]:
    table_corres[k] = f"ingame/{k}.png"

for bt in putain_de_bt.keys():
    table_corres[bt] = f"ingame/{bt}.png"




if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
