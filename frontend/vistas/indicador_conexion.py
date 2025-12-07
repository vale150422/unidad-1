"""
Widget indicador de estado de conexión para Tkinter
Muestra una luz verde/roja y cuenta regresiva para el próximo backup
"""

import tkinter as tk
from tkinter import Canvas
import threading
import time

class IndicadorConexion(tk.Frame):
    """
    Widget que muestra:
    - Luz verde/roja de estado de conexión
    - Contador regresivo para el próximo backup/verificación
    """
    
    def __init__(self, parent, monitor_conexion=None, intervalo_verificacion=5):
        """
        Args:
            parent: Widget padre
            monitor_conexion: Instancia de MonitorConexion
            intervalo_verificacion: Segundos entre verificaciones
        """
        super().__init__(parent, bg="lightgray", height=60)
        self.pack_propagate(False)
        
        self.monitor = monitor_conexion
        self.intervalo_verificacion = intervalo_verificacion
        self.tiempo_restante = intervalo_verificacion
        self.hilo_contador = None
        self.activo = False
        
        # Frame contenedor
        contenedor = tk.Frame(self, bg="lightgray")
        contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para el indicador visual (círculo rojo/verde)
        self.canvas = Canvas(
            contenedor,
            width=30,
            height=30,
            bg="lightgray",
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, padx=5)
        
        # Dibujar círculo inicial (rojo = desconectado)
        self._dibujar_circulo(False)
        
        # Frame para información
        info_frame = tk.Frame(contenedor, bg="lightgray")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Label de estado
        self.label_estado = tk.Label(
            info_frame,
            text="Desconectado",
            font=("Arial", 10, "bold"),
            bg="lightgray",
            fg="red"
        )
        self.label_estado.pack(anchor=tk.W)
        
        # Label de información
        self.label_info = tk.Label(
            info_frame,
            text="Próxima verificación en 5s",
            font=("Arial", 9),
            bg="lightgray",
            fg="gray"
        )
        self.label_info.pack(anchor=tk.W)
        
        # Label de hora última verificación
        self.label_hora = tk.Label(
            info_frame,
            text="Última verificación: Nunca",
            font=("Arial", 8),
            bg="lightgray",
            fg="darkgray"
        )
        self.label_hora.pack(anchor=tk.W)
        
        # Registrar callback si hay monitor
        if self.monitor:
            self.monitor.registrar_callback(self._on_cambio_conexion)
        
        # Iniciar contador
        self.iniciar_contador()
    
    def _dibujar_circulo(self, conectado):
        """
        Dibuja un círculo en el canvas
        
        Args:
            conectado: True para verde, False para rojo
        """
        self.canvas.delete("all")
        
        # Color según estado
        color = "lime" if conectado else "red"
        
        # Dibujar círculo
        self.canvas.create_oval(
            2, 2, 28, 28,
            fill=color,
            outline="black",
            width=2
        )
        
        # Añadir efecto de brillo si está conectado
        if conectado:
            self.canvas.create_oval(
                5, 5, 12, 12,
                fill="white",
                outline="",
            )
    
    def _on_cambio_conexion(self, conectado, timestamp):
        """
        Callback ejecutado cuando cambia el estado de conexión
        
        Args:
            conectado: True si está conectado
            timestamp: Hora de la verificación
        """
        # Actualizar desde el hilo del monitor
        self.actualizar_estado(conectado, timestamp)
    
    def actualizar_estado(self, conectado, timestamp=None):
        """
        Actualiza el estado visual
        
        Args:
            conectado: True si está conectado
            timestamp: Datetime de la última verificación
        """
        # Actualizar círculo
        self._dibujar_circulo(conectado)
        
        # Actualizar labels
        if conectado:
            self.label_estado.config(text="✓ Conectado", fg="green")
        else:
            self.label_estado.config(text="✗ Desconectado", fg="red")
        
        # Actualizar hora de última verificación
        if timestamp:
            hora_str = timestamp.strftime("%H:%M:%S")
            self.label_hora.config(text=f"Última verificación: {hora_str}")
    
    def iniciar_contador(self):
        """Inicia el contador regresivo"""
        if self.activo:
            return
        
        self.activo = True
        self.tiempo_restante = self.intervalo_verificacion
        self.hilo_contador = threading.Thread(
            target=self._contador_loop,
            daemon=True
        )
        self.hilo_contador.start()
    
    def detener_contador(self):
        """Detiene el contador"""
        self.activo = False
        if self.hilo_contador:
            self.hilo_contador.join(timeout=2)
    
    def _contador_loop(self):
        """Loop del contador regresivo"""
        while self.activo:
            try:
                # Actualizar label (de forma segura en Tkinter)
                self.label_info.config(
                    text=f"Próxima verificación en {self.tiempo_restante}s"
                )
                
                self.tiempo_restante -= 1
                
                if self.tiempo_restante < 0:
                    self.tiempo_restante = self.intervalo_verificacion
                
                time.sleep(1)
            
            except tk.TclError:
                # Widget fue destruido
                break
            except Exception as e:
                print(f"Error en contador: {e}")
    
    def destroy(self):
        """Limpia recursos al destruir el widget"""
        self.detener_contador()
        super().destroy()
