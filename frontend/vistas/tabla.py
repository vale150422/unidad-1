import tkinter as tk
from tkinter import ttk


class Tabla(ttk.Treeview):
    """
    Componente de tabla reutilizable para el sistema IHEP.

    Esta clase extiende ttk.Treeview y proporciona:
    - Creación automática de encabezados
    - Scrollbar vertical integrado
    - Métodos para limpiar, cargar y obtener filas
    - Un alias 'agregar' para compatibilidad con las vistas MVC

    Se utiliza en las vistas de Herramientas, Préstamos y Búsqueda.
    """

    def __init__(self, parent, columnas, *args, **kwargs):
        """
        Inicializa la tabla con columnas dinámicas y un scrollbar vertical.

        Parámetros:
            parent  -- widget padre
            columnas -- lista de nombres de columnas para la tabla
        """
        super().__init__(parent, columns=columnas, show="headings", *args, **kwargs)

        # Crear encabezados con ancho base
        for col in columnas:
            self.heading(col, text=col)
            self.column(col, width=120)

        # Scrollbar vertical
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetado
        self.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # -----------------------
    #   MÉTODOS PÚBLICOS
    # -----------------------

    def limpiar(self):
        """Borra todas las filas actuales de la tabla."""
        for item in self.get_children():
            self.delete(item)

    def agregar_fila(self, valores):
        """Agrega una nueva fila con los valores proporcionados."""
        self.insert("", "end", values=valores)

    def agregar(self, *valores):
        """
        Alias para agregar_fila.

        Este método existe para compatibilidad con las vistas del sistema,
        que utilizan 'tabla.agregar(...)' como interfaz genérica.
        """
        self.insert("", "end", values=valores)

    def obtener_todo(self):
        """
        Retorna todas las filas actualmente mostradas en la tabla.

        Devuelve:
            Lista de listas, donde cada elemento son los valores de una fila.
        """
        datos = []
        for item in self.get_children():
            datos.append(self.item(item)["values"])
        return datos

    def cargar_datos(self, filas):
        """
        Limpia la tabla e inserta un conjunto completo de nuevas filas.

        Parámetros:
            filas -- iterable con elementos que representan cada fila
        """
        self.limpiar()
        for fila in filas:
            self.insert("", "end", values=fila)

    def index(self, item_id):
        """
        Retorna el índice (posición) de un item en la tabla.
        
        Parámetros:
            item_id -- ID del item retornado por selection()
        
        Devuelve:
            Índice numérico (0, 1, 2, ...) o None si no existe
        """
        try:
            all_items = self.get_children()
            return all_items.index(item_id)
        except (ValueError, IndexError):
            return None
