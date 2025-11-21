import tkinter as tk
from tkinter import ttk, messagebox
from .db import get_connection

class EnvioFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bd=8)
        self.controller = controller

        header = tk.Frame(self)
        header.pack(fill="x")
        tk.Label(header, text="RF5 - Envío de Productos", font=("Arial", 18, "bold")).pack(side="left", padx=10, pady=10)
        ttk.Button(header, text="Volver al menú", command=lambda: controller.show("MenuFrame")).pack(side="right", padx=10)

        # --- Selección de factura ---
        factura_box = tk.LabelFrame(self, text="Seleccionar factura", padx=8, pady=8)
        factura_box.pack(fill="x", padx=10, pady=10)

        self.factura_var = tk.StringVar()
        self.factura_menu = ttk.Combobox(factura_box, textvariable=self.factura_var, state="readonly")
        self.factura_menu.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(factura_box, text="Cargar productos", command=self.cargar_productos).pack(side="right", padx=5)

        # --- Tabla productos ---
        productos_box = tk.LabelFrame(self, text="Productos de la factura", padx=8, pady=8)
        productos_box.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id","detalle","estado")
        self.tree = ttk.Treeview(productos_box, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c.upper())
        self.tree.pack(fill="both", expand=True)

        ttk.Button(self, text="Despachar producto", command=self.despachar_producto).pack(pady=10)

        # Se ejecutará cuando el frame se muestre
        self.bind("<<ShowFrame>>", lambda e: self.cargar_facturas())

    # Para que <<ShowFrame>> se dispare al levantar el frame
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.event_generate("<<ShowFrame>>")

    def cargar_facturas(self):
        # AHORA: trae todas las facturas, no exige que haya registros en envios
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT id, orden_id, total
                FROM facturas
                ORDER BY id DESC
            """).fetchall()

        opciones = [f"ID {r['id']} - Orden {r['orden_id']} - Total ${r['total']}" for r in rows]
        self.factura_menu['values'] = opciones
        if opciones:
            self.factura_menu.current(0)
        else:
            self.factura_var.set("")

        # Limpia la tabla de productos
        self.tree.delete(*self.tree.get_children())

    def cargar_productos(self):
        seleccionado = self.factura_var.get()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione una factura")
            return

        factura_id = int(seleccionado.split()[1])

        with get_connection() as conn:
            productos = conn.execute("""
                SELECT id, detalle, estado_envio
                FROM envios
                WHERE factura_id=?
            """, (factura_id,)).fetchall()

        self.tree.delete(*self.tree.get_children())
        for p in productos:
            self.tree.insert("", "end", values=(p["id"], p["detalle"], p["estado_envio"]))

    def despachar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione un producto")
            return

        producto_id = self.tree.item(selected[0])['values'][0]

        with get_connection() as conn:
            conn.execute("UPDATE envios SET estado_envio='despachado' WHERE id=?", (producto_id,))
            conn.commit()

        messagebox.showinfo("Éxito", f"Producto {producto_id} despachado")
        self.cargar_productos()
