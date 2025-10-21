import tkinter as tk
from tkinter import messagebox
from .db import init_db
from .login import LoginFrame
from .menu import MenuFrame
from .orden_compra import OrdenFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema OC - Facturación - Envío")
        self.geometry("900x600")
        self.resizable(False, False)


        self.session_user = None

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginFrame, MenuFrame, OrdenFrame):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("LoginFrame")

    def show(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def set_user(self, username):
        self.session_user = username

    def get_user(self):
        return self.session_user

def main():
    init_db()
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
