# vistas/vista_busqueda.py
"""
VistaBusqueda
--------------
Esta vista permite realizar búsquedas globales dentro de la aplicación, combinando
información proveniente de herramientas y préstamos. Forma parte de la capa de 
presentación dentro de la arquitectura MVC utilizada en el frontend Tkinter.

La vista muestra:
- Un campo de búsqueda
- Botones para buscar y mostrar toda la información
- Una tabla que mezcla datos provenientes de las vistas hijas:
    * VistaHerramientas
    * VistaPrestamos

La vista no se comunica directamente con el backend; en su lugar solicita 
a las otras vistas que actualicen sus datos mediante sus propios métodos.
"""

from tkinter import Frame, Label, Entry, Button, StringVar
from vistas.tabla import Tabla


class VistaBusqueda(Frame):
    """
    Clase que representa la vista de búsqueda global dentro del sistema.
    Permite filtrar tanto herramientas como préstamos usando un único campo.

    Parámetros:
    - parent: contenedor padre dentro de Tkinter.
    - vista_herramientas: referencia a la vista que maneja herramientas.
    - vista_prestamos: referencia a la vista que maneja préstamos.
    """

    def __init__(self, parent, vista_herramientas, vista_prestamos):
        super().__init__(parent)

        # Referencias a otras vistas para obtener datos y sincronizar con backend
        self.vista_herramientas = vista_herramientas
        self.vista_prestamos = vista_prestamos

        # Título de la sección
        Label(self, text="Búsqueda", font=("Arial", 14)).pack(pady=10)

        # Frame que contiene el campo de texto y botones
        filtro_frame = Frame(self)
        filtro_frame.pack(pady=6)

        Label(
            filtro_frame,
            text="Buscar (código, nombre, categoría o responsable)"
        ).grid(row=0, column=0, padx=5)

        # Campo de entrada para el término de búsqueda
        self.entrada_var = StringVar()
        Entry(
            filtro_frame, textvariable=self.entrada_var, width=40
        ).grid(row=0, column=1, padx=6)

        # Botón buscar
        Button(
            filtro_frame, text="Buscar", command=self.buscar
        ).grid(row=0, column=2, padx=6)

        # Botón para mostrar todos los elementos
        Button(
            filtro_frame, text="Mostrar todo", command=self.mostrar_todo
        ).grid(row=0, column=3, padx=6)

        # Tabla donde se mostrarán los resultados de herramientas y préstamos
        columnas = ["Origen", "Código", "Nombre/Responsable", "Detalle"]
        self.tabla = Tabla(self, columnas)

        # Al iniciar: sincroniza datos desde backend y carga todo en tabla
        self._recargar_datos_backend()
        self.mostrar_todo()

    # ----------------------------------------------------------------------
    # Sincronización de datos con el backend
    # ----------------------------------------------------------------------
    def _recargar_datos_backend(self):
        """
        Solicita a las vistas hijas que vuelvan a consultar el backend.
        Esto asegura que los datos mostrados estén siempre actualizados.
        """
        try:
            self.vista_herramientas.cargar_datos_backend()
        except:
            pass  # Si alguna vista no tiene método, simplemente se ignora

        try:
            self.vista_prestamos.cargar_datos_backend()
        except:
            pass

    # ----------------------------------------------------------------------
    # Acceso a los datos provenientes de otras vistas
    # ----------------------------------------------------------------------
    def obtener_herramientas(self):
        """
        Retorna la lista actual de herramientas cargadas por la vista de herramientas.
        """
        return self.vista_herramientas.lista_herramientas

    def obtener_prestamos(self):
        """
        Retorna la lista actual de préstamos, obtenida desde la vista de préstamos.
        """
        return self.vista_prestamos.obtener_filas()

    # ----------------------------------------------------------------------
    # Mostrar todos los registros
    # ----------------------------------------------------------------------
    def mostrar_todo(self):
        """
        Carga en la tabla todos los registros de herramientas y préstamos,
        sin aplicar ningún filtro.
        """
        # Actualiza datos primero
        self._recargar_datos_backend()

        data = []

        # Agrega herramientas a la tabla
        for h in self.obtener_herramientas():
            data.append((
                "Herramienta",
                h["codigo"],
                h["nombre"],
                h["estado"]
            ))

        # Agrega préstamos a la tabla
        for p in self.obtener_prestamos():
            data.append((
                "Préstamo",
                p["numero"],
                p["responsable"],
                p["herramienta_codigo"]
            ))

        # Cargar los datos combinados en la tabla
        self.tabla.cargar_datos(data)

    # ----------------------------------------------------------------------
    # Búsqueda filtrada
    # ----------------------------------------------------------------------
    def buscar(self):
        """
        Filtra los registros usando el texto ingresado por el usuario.
        Permite buscar por código, nombre, categoría (herramientas),
        responsable o código de herramienta (préstamos).
        """
        termino = self.entrada_var.get().strip().lower()

        # Si el campo está vacío, se muestra todo
        if not termino:
            self.mostrar_todo()
            return

        # Actualizar datos antes de filtrar
        self._recargar_datos_backend()

        resultados = []

        # Filtro de herramientas
        for h in self.obtener_herramientas():
            if (
                termino in h["codigo"].lower() or
                termino in h["nombre"].lower() or
                termino in h["categoria"].lower()
            ):
                resultados.append((
                    "Herramienta",
                    h["codigo"],
                    h["nombre"],
                    h["estado"]
                ))

        # Filtro de préstamos
        for p in self.obtener_prestamos():
            if (
                termino in p["numero"].lower() or
                termino in p["herramienta_codigo"].lower() or
                termino in p["responsable"].lower()
            ):
                resultados.append((
                    "Préstamo",
                    p["numero"],
                    p["responsable"],
                    p["herramienta_codigo"]
                ))

        # Cargar los resultados filtrados
        self.tabla.cargar_datos(resultados)
