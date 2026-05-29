import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import os, re
import shutil, zipfile
from datetime import datetime

from src.fetchdata import get_chara_from_str, get_move_data, get_move_img_from_data
from src.NoteTab import NoteTab
from src.ProfileWindow import ProfileWindow
from src.SelectChara import SelectChara
from src.SheetTab import SheetTab
from src.CustomizationWindow import CustomizationWindow
from src.NotesApp import NotesApp


if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
