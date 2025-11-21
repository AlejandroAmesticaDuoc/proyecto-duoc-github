import tkinter as tk
from tkinter import ttk, messagebox
from .db import get_connection

class OrdenFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bd=8)
        self.controller = controller

        header = tk.Frame(self)
        header.pack(fill="x")
        tk.Label(header, text="Órdenes de Compra", font=("Arial", 18, "bold")).pack(side="left", padx=10, pady=10)
        ttk.Button(header, text="Volver al Menú", command=lambda: controller.show("MenuFrame")).pack(side="right", padx=10)


        form = tk.LabelFrame(self, text="Nueva Orden", padx=8, pady=8)
        form.pack(fill="x", padx=10, pady=6)

        self.vars = {k: tk.StringVar() for k in [
            "numero_orden","cliente","direccion","telefono","comuna","region","productos","precios"
        ]}

        def add_row(row, label, key):
            tk.Label(form, text=label).grid(row=row, column=0, sticky="e", padx=6, pady=4)
            ttk.Entry(form, textvariable=self.vars[key], width=50).grid(row=row, column=1, padx=6, pady=4)

        add_row(0, "N° Orden", "numero_orden")
        add_row(1, "Cliente", "cliente")
        add_row(2, "Dirección", "direccion")
        add_row(3, "Teléfono", "telefono")
        add_row(4, "Comuna", "comuna")
        add_row(5, "Región", "region")
        add_row(6, "Productos (lista simple)", "productos")
        add_row(7, "Precios (lista simple)", "precios")

        ttk.Button(form, text="Guardar", command=self.guardar).grid(row=8, column=1, sticky="w", padx=6, pady=8)


        table_box = tk.LabelFrame(self, text="Órdenes registradas", padx=8, pady=8)
        table_box.pack(fill="both", expand=True, padx=10, pady=8)

        cols = ("id","numero_orden","cliente","estado")
        self.tree = ttk.Treeview(table_box, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=150 if c != "cliente" else 220)
        self.tree.pack(fill="both", expand=True)

        self.bind("<<ShowFrame>>", lambda e: self.cargar_ordenes())

    def guardar(self):
        data = {k: v.get().strip() for k, v in self.vars.items()}
        if not all(data.values()):
            messagebox.showwarning("Órdenes", "Completa todos los campos.")
            return

        with get_connection() as conn:
            conn.execute("""
                INSERT INTO ordenes_compra
                (numero_orden, cliente, direccion, telefono, comuna, region, productos, precios)
                VALUES (:numero_orden, :cliente, :direccion, :telefono, :comuna, :region, :productos, :precios)
            """, data)
            conn.commit()

        messagebox.showinfo("Órdenes", "Orden guardada.")
        for v in self.vars.values():
            v.set("")
        self.cargar_ordenes()

    def cargar_ordenes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        with get_connection() as conn:
            rows = conn.execute("SELECT id, numero_orden, cliente, estado FROM ordenes_compra ORDER BY id DESC").fetchall()
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["numero_orden"], r["cliente"], r["estado"]))

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.event_generate("<<ShowFrame>>")
