import tkinter as tk

from db.base import create_db_engine
from db.models import create_tables
from interface.auth_screen import Interface

if __name__ == "__main__":
    root = tk.Tk()
    interface = Interface(root)
    root.mainloop()
