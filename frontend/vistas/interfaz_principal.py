# vistas/interfaz_principal.py
"""
Interfaz principal del sistema IHEP

Esta clase crea la ventana principal de la aplicación y carga las tres
vistas principales del sistema:

- Herramientas
- Préstamos
- Búsqueda Global

También inicializa:
- Monitor de conexión con threading
- Indicador visual de estado de conexión
- Contador regresivo de verificación
"""

import tkinter as tk
from tkinter import ttk

from vistas.vista_herramientas import VistaHerramientas
from vistas.vista_prestamos import VistaPrestamos
from vistas.vista_busqueda import VistaBusqueda
from vistas.indicador_conexion import IndicadorConexion
from controladores.monitor_conexion import MonitorConexion
from controladores.respaldo import RespaldoAutomatico


class InterfazPrincipal(tk.Tk):
    """
    Ventana principal de la aplicación IHEP.
    Contiene el sistema de pestañas y administra la carga inicial de datos.
    Incluye monitoreo de conexión en segundo plano.
    """

    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.title("IHEP - Sistema de Inventario de Herramientas y Préstamos")
        self.geometry("900x700")

        # Inicializar monitor de conexión
        self.monitor_conexion = MonitorConexion(
            api_url="http://127.0.0.1:8000/api",
            intervalo=5  # Verificar cada 5 segundos
        )
        self.monitor_conexion.iniciar()

        # Inicializar respaldo automático
        self.respaldo = RespaldoAutomatico(
            api_url="http://127.0.0.1:8000/api",
            intervalo_segundos=None  # Lee INTERVALO_BACKUP_SEG o usa 300 seg default
        )
        self.respaldo.iniciar()

        # Crear indicador de conexión
        self._crear_indicador_conexion()

        # Crear pestañas principales
        self._crear_pestanas()

        # Intentar cargar datos desde el backend
        try:
            self.herramientas.cargar_datos_backend()
        except:
            pass

        try:
            self.prestamos.cargar_datos_backend()
        except:
            pass

        # Limpiar recursos al cerrar
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _crear_indicador_conexion(self):
        """Crea y configura el indicador visual de conexión"""
        self.indicador = IndicadorConexion(
            self,
            monitor_conexion=self.monitor_conexion,
            intervalo_verificacion=5
        )
        self.indicador.pack(fill=tk.X, side=tk.TOP)

    def _crear_pestanas(self):
        """
        Crea el contenedor Notebook y registra las vistas del sistema:
        - Herramientas
        - Préstamos
        - Búsqueda
        """

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Instanciar vistas principales
        self.herramientas = VistaHerramientas(notebook)
        self.prestamos = VistaPrestamos(notebook)

        # Vista de búsqueda necesita acceder a las otras dos
        self.busqueda = VistaBusqueda(notebook, self.herramientas, self.prestamos)

        # Registrar cada vista como una pestaña
        notebook.add(self.herramientas, text="Herramientas")
        notebook.add(self.prestamos, text="Préstamos")
        notebook.add(self.busqueda, text="Búsqueda")

    def _on_close(self):
        """Limpia recursos antes de cerrar la aplicación"""
        try:
            self.monitor_conexion.detener()
            self.indicador.detener_contador()
            self.respaldo.detener()
        except:
            pass
        
        self.destroy()
