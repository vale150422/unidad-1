# vistas/vista_busqueda.py

from tkinter import Frame, Label, Entry, Button, StringVar
from vistas.tabla import Tabla


class VistaBusqueda(Frame):

    def __init__(self, parent, vista_herramientas, vista_prestamos):
        super().__init__(parent)

        # referencias a las otras vistas
        self.vista_herramientas = vista_herramientas
        self.vista_prestamos = vista_prestamos

        Label(self, text="Búsqueda", font=("Arial", 14)).pack(pady=10)

        filtro_frame = Frame(self)
        filtro_frame.pack(pady=6)

        Label(filtro_frame, text="Buscar (código, nombre, categoría o responsable)").grid(row=0, column=0, padx=5)
        self.entrada_var = StringVar()
        Entry(filtro_frame, textvariable=self.entrada_var, width=40).grid(row=0, column=1, padx=6)

        Button(filtro_frame, text="Buscar", command=self.buscar).grid(row=0, column=2, padx=6)
        Button(filtro_frame, text="Mostrar todo", command=self.mostrar_todo).grid(row=0, column=3, padx=6)

        columnas = ["Origen", "Código", "Nombre/Responsable", "Detalle"]
        self.tabla = Tabla(self, columnas)

        # Recargar todo desde el backend al iniciar
        self._recargar_datos_backend()
        self.mostrar_todo()

    # --------------------------
    # Recargar datos desde API
    # --------------------------
    def _recargar_datos_backend(self):
        """Fuerza a que las vistas hijas actualicen con la API antes de usar los datos"""
        try:
            self.vista_herramientas.cargar_datos_backend()
        except:
            pass

        try:
            self.vista_prestamos.cargar_datos_backend()
        except:
            pass

    # --------------------------
    # Obtener datos reales
    # --------------------------
    def obtener_herramientas(self):
        return self.vista_herramientas.lista_herramientas

    def obtener_prestamos(self):
        return self.vista_prestamos.obtener_filas()

    # --------------------------
    # Mostrar todo
    # --------------------------
    def mostrar_todo(self):
        # Recargar datos actuales desde el backend
        self._recargar_datos_backend()

        data = []

        # herramientas
        for h in self.obtener_herramientas():
            data.append(("Herramienta", h["codigo"], h["nombre"], h["estado"]))

        # préstamos
        for p in self.obtener_prestamos():
            data.append(("Préstamo", p["numero"], p["responsable"], p["herramienta_codigo"]))

        self.tabla.cargar_datos(data)

    # --------------------------
    # Buscar
    # --------------------------
    def buscar(self):
        termino = self.entrada_var.get().strip().lower()
        if not termino:
            self.mostrar_todo()
            return

        # Recargar datos actuales desde backend
        self._recargar_datos_backend()

        resultados = []

        # herramientas
        for h in self.obtener_herramientas():
            if (termino in h["codigo"].lower() or
                termino in h["nombre"].lower() or
                termino in h["categoria"].lower()):
                resultados.append(("Herramienta", h["codigo"], h["nombre"], h["estado"]))

        # préstamos
        for p in self.obtener_prestamos():
            if (termino in p["numero"].lower() or
                termino in p["herramienta_codigo"].lower() or
                termino in p["responsable"].lower()):
                resultados.append(("Préstamo", p["numero"], p["responsable"], p["herramienta_codigo"]))

        self.tabla.cargar_datos(resultados)
