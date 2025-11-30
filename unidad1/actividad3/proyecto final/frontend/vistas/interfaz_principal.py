# vistas/interfaz_principal.py
"""
Ventana principal del sistema IHEP
Muestra las pestañas:
- Herramientas
- Préstamos
- Búsqueda
"""

import tkinter as tk
from tkinter import ttk

from vistas.vista_herramientas import VistaHerramientas
from vistas.vista_prestamos import VistaPrestamos
from vistas.vista_busqueda import VistaBusqueda


class InterfazPrincipal(tk.Tk):
    """Ventana principal con pestañas del sistema IHEP."""

    def __init__(self):
        super().__init__()

        self.title("IHEP - Sistema de Inventario de Herramientas y Préstamos")
        self.geometry("900x600")

        self._crear_pestanas()

        # ----------------------------
        # CARGAR DATOS DEL BACKEND
        # ----------------------------
        try:
            self.herramientas.cargar_datos_backend()
        except:
            pass

        try:
            self.prestamos.cargar_datos_backend()
        except:
            pass

    def _crear_pestanas(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Crear vistas principales primero
        self.herramientas = VistaHerramientas(notebook)
        self.prestamos = VistaPrestamos(notebook)

        # AHORA sí puedes pasar estas dos vistas a VistaBusqueda
        self.busqueda = VistaBusqueda(notebook, self.herramientas, self.prestamos)

        # Agregar pestañas
        notebook.add(self.herramientas, text="Herramientas")
        notebook.add(self.prestamos, text="Préstamos")
        notebook.add(self.busqueda, text="Búsqueda")
