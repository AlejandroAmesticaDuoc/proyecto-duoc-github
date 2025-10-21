import tkinter as tk
from tkinter import ttk, messagebox
from .db import get_connection

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bd=8)
        self.controller = controller

        tk.Label(self, text="Iniciar Sesión", font=("Arial", 18, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Usuario").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        tk.Label(form, text="Contraseña").grid(row=1, column=0, sticky="e", padx=6, pady=6)

        self.user_var = tk.StringVar()
        self.pwd_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.user_var, width=30).grid(row=0, column=1, padx=6, pady=6)
        ttk.Entry(form, textvariable=self.pwd_var, show="*", width=30).grid(row=1, column=1, padx=6, pady=6)

        ttk.Button(self, text="Entrar", command=self.on_login).pack(pady=10)

    def on_login(self):
        user = self.user_var.get().strip()
        pwd = self.pwd_var.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Login", "Completa usuario y contraseña.")
            return

        with get_connection() as conn:
            row = conn.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (user, pwd)).fetchone()

        if row:
            self.controller.set_user(row["username"])
            self.controller.show("MenuFrame")
        else:
            messagebox.showerror("Login", "Credenciales inválidas")
