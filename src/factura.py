import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .db import get_connection

class FacturaFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bd=8)
        self.controller = controller

        header = tk.Frame(self)
        header.pack(fill="x")
        tk.Label(header, text="Emisión de Facturas", font=("Arial", 18, "bold")).pack(side="left", padx=10, pady=10)
        ttk.Button(header, text="Volver al menú", command=lambda: controller.show("MenuFrame")).pack(side="right", padx=10)

        box = tk.LabelFrame(self, text="Órdenes disponibles para facturar", padx=8, pady=8)
        box.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id","numero","cliente","estado")
        self.tree = ttk.Treeview(box, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c.upper())
        self.tree.pack(fill="both", expand=True)

        ttk.Button(self, text="Emitir Factura", command=self.emitir_factura).pack(pady=10)

        self.bind("<<ShowFrame>>", lambda e: self.cargar_ordenes())

    def cargar_ordenes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        with get_connection() as conn:
            rows = conn.execute("""
                SELECT id, numero_orden, cliente, estado 
                FROM ordenes_compra 
                WHERE estado = 'ingresada'
            """).fetchall()

        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["numero_orden"], r["cliente"], r["estado"]))

    def emitir_factura(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Factura", "Selecciona una orden.")
            return

        item = self.tree.item(selected[0])
        orden_id = item["values"][0]

        with get_connection() as conn:
            orden = conn.execute("SELECT * FROM ordenes_compra WHERE id=?", (orden_id,)).fetchone()


        precios = orden["precios"].split(",")
        subtotal = sum(float(p.strip()) for p in precios)

        iva = round(subtotal * 0.19, 2)
        total = round(subtotal + iva, 2)

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with get_connection() as conn:
            conn.execute("""
                INSERT INTO facturas (orden_id, subtotal, iva, total, fecha)
                VALUES (?, ?, ?, ?, ?)
            """, (orden_id, subtotal, iva, total, fecha))

            conn.execute("""
                UPDATE ordenes_compra SET estado='facturada' WHERE id=?
            """, (orden_id,))

            conn.commit()

        messagebox.showinfo("Factura emitida", 
            f"Factura generada:\n\nSubtotal: ${subtotal}\nIVA (19%): ${iva}\nTotal: ${total}")

        self.cargar_ordenes()

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.event_generate("<<ShowFrame>>")
