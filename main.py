import tkinter as tk

from db.base import create_db_engine, get_db, create_tables, delete_tables  # noqa
from interface.interface_manager import InterfaceManager
from interface.auth_screen import AuthInterface

if __name__ == "__main__":
    engine = create_db_engine()
    # create_tables(engine)  #  Использовать только при первом запуске программы
    # delete_tables(engine)  #  Использовать для удаления всех таблиц из базы данных
    root = tk.Tk()
    photo = tk.PhotoImage(file="Kurama.png")
    root.iconphoto(False, photo)
    root.title("ArtHive")
    root.geometry("1024x700+500+400")
    root.minsize(400, 400)
    root.config(bg="#FFFFFF")
    with get_db(engine) as session:
        manager = InterfaceManager(root, session)
        manager.show_interface(AuthInterface)
    root.mainloop()
