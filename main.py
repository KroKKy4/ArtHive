import tkinter as tk

from db.base import create_db_engine
from db.models import create_tables
from db.base import get_db
from interface.interface_manager import InterfaceManager
from interface.auth_screen import AuthInterface

if __name__ == "__main__":
    engine = create_db_engine()
    # create_tables(engine) #  Использовать только при первом запуске программы
    root = tk.Tk()
    root.title("ArtHive")
    root.geometry("1024x600+500+400")
    root.minsize(400, 400)
    root.config(bg="#FFFFFF")
    with get_db(engine) as session:
        manager = InterfaceManager(root, session)
        manager.show_interface(AuthInterface)
    root.mainloop()
