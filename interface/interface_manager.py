import tkinter as tk
from tkinter import ttk

from interface.auth_screen import AuthInterface
from interface.main_screen import MainInterface


class InterfaceManager:
    def __init__(self, master):
        self.master = master
        self.current_interface = None

    def show_interface(self, interface_class, user=None, *args, **kwargs):
        if self.current_interface:
            self.current_interface.destroy()
        self.current_interface = interface_class(
            self.master, self, user, self.main_window, *args, **kwargs
        )
        self.current_interface.pack(fill=tk.BOTH, expand=True)

    def login_success(self, user):
        self.show_interface(MainInterface, user=user)

    def logout_success(self):
        self.show_interface(AuthInterface)

    def main_window(self):
        self.show_interface(MainInterface)
