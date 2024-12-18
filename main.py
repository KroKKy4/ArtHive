import tkinter as tk

from db.base import create_db_engine
from db.models import create_tables
from interface.interface_manager import InterfaceManager
from interface.auth_screen import AuthInterface

if __name__ == "__main__":
    # engine = create_db_engine() #  Функции для создания таблиц
    # create_tables(engine) #  Использовать только при первом запуске программы
    root = tk.Tk()
    root.title("ArtHive")
    root.geometry("1024x600")
    root.config(bg="#FFFFFF")
    manager = InterfaceManager(root)
    manager.show_interface(AuthInterface)
    root.mainloop()
