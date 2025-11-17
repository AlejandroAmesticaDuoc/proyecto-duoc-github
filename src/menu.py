import tkinter as tk
from tkinter import ttk, messagebox

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bd=8)
        self.controller = controller

        header = tk.Frame(self)
        header.pack(fill="x")
        tk.Label(header, text="Menú Principal", font=("Arial", 18, "bold")).pack(side="left", padx=10, pady=10)

        self.user_lbl = tk.Label(header, text="", font=("Arial", 10))
        self.user_lbl.pack(side="right", padx=10)

        nav = tk.Frame(self)
        nav.pack(pady=10)
        ttk.Button(nav, text="Home", command=self._home).grid(row=0, column=0, padx=6)
        ttk.Button(nav, text="Órdenes de Compra", command=lambda: controller.show("OrdenFrame")).grid(row=0, column=1, padx=6)
        ttk.Button(nav, text="Cerrar sesión", command=self._logout).grid(row=0, column=2, padx=6)
        ttk.Button(nav, text="Facturación", command=lambda: controller.show("FacturaFrame")).grid(row=0, column=3, padx=6)

        self.msg = tk.Label(self, text="Bienvenido/a", font=("Arial", 12))
        self.msg.pack(pady=20)

        self.bind("<<ShowFrame>>", self.on_show)

    def on_show(self, _event=None):
        user = self.controller.get_user()
        if not user:
            self.controller.show("LoginFrame")
            return
        self.user_lbl.config(text=f"Usuario: {user}")
        self.msg.config(text=f"Bienvenido/a, {user}")

    def _home(self):
        messagebox.showinfo("Home", "Estás en Home.")

    def _logout(self):
        self.controller.set_user(None)
        self.controller.show("LoginFrame")

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.event_generate("<<ShowFrame>>")
