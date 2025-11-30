import tkinter as tk
from tkinter import ttk


class Tabla(ttk.Treeview):

    def __init__(self, parent, columnas, *args, **kwargs):
        super().__init__(parent, columns=columnas, show="headings", *args, **kwargs)

        # Crear encabezados
        for col in columnas:
            self.heading(col, text=col)
            self.column(col, width=120)

        # Scroll vertical
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)

        # Pack
        self.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # -----------------------
    #   MÉTODOS NECESARIOS
    # -----------------------

    def limpiar(self):
        """Borra todas las filas."""
        for item in self.get_children():
            self.delete(item)

    def agregar_fila(self, valores):
        """Agrega una fila nueva."""
        self.insert("", "end", values=valores)

    # 🔥 MÉTODO QUE USAN LAS VISTAS (requerido)
    def agregar(self, *valores):
        """Alias para agregar_fila, compatible con las vistas."""
        self.insert("", "end", values=valores)

    def obtener_todo(self):
        """Retorna todos los registros actuales."""
        datos = []
        for item in self.get_children():
            datos.append(self.item(item)["values"])
        return datos

    def cargar_datos(self, filas):
        """Borra la tabla y carga nuevas filas."""
        self.limpiar()
        for fila in filas:
            self.insert("", "end", values=fila)
