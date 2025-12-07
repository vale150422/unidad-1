"""
Módulo de monitoreo de conexión backend-frontend
Usa threading para verificar la conexión sin bloquear la UI
"""

import threading
import requests
import time
from datetime import datetime

class MonitorConexion:
    """
    Monitorea la conexión con el backend en un hilo separado
    """
    
    def __init__(self, api_url="http://127.0.0.1:8000/api", intervalo=5):
        """
        Args:
            api_url: URL base de la API
            intervalo: Segundos entre verificaciones (default: 5)
        """
        self.api_url = api_url
        self.intervalo = intervalo
        self.conectado = False
        self.ultima_verificacion = None
        self.hilo = None
        self.activo = False
        self.callbacks = []  # Lista de funciones a llamar cuando cambia el estado
        
    def registrar_callback(self, callback):
        """
        Registra una función para ejecutar cuando cambia el estado de conexión
        
        Args:
            callback: Función que recibe (conectado, timestamp)
        """
        self.callbacks.append(callback)
    
    def iniciar(self):
        """Inicia el monitoreo en un hilo separado"""
        if self.activo:
            return
        
        self.activo = True
        self.hilo = threading.Thread(target=self._verificar_conexion_loop, daemon=True)
        self.hilo.start()
    
    def detener(self):
        """Detiene el monitoreo"""
        self.activo = False
        if self.hilo:
            self.hilo.join(timeout=2)
    
    def _verificar_conexion_loop(self):
        """Loop que verifica la conexión periódicamente"""
        while self.activo:
            try:
                # Intentar hacer una petición simple a la API
                respuesta = requests.get(
                    f"{self.api_url}/herramientas/",
                    timeout=2
                )
                
                estado_anterior = self.conectado
                self.conectado = respuesta.status_code < 500
                self.ultima_verificacion = datetime.now()
                
                # Si cambió el estado, ejecutar callbacks
                if estado_anterior != self.conectado:
                    for callback in self.callbacks:
                        try:
                            callback(self.conectado, self.ultima_verificacion)
                        except Exception as e:
                            print(f"Error en callback: {e}")
            
            except (requests.ConnectionError, requests.Timeout):
                estado_anterior = self.conectado
                self.conectado = False
                self.ultima_verificacion = datetime.now()
                
                # Si cambió el estado, ejecutar callbacks
                if estado_anterior != self.conectado:
                    for callback in self.callbacks:
                        try:
                            callback(self.conectado, self.ultima_verificacion)
                        except Exception as e:
                            print(f"Error en callback: {e}")
            
            except Exception as e:
                print(f"Error verificando conexión: {e}")
            
            # Esperar antes de la siguiente verificación
            time.sleep(self.intervalo)
    
    def obtener_estado(self):
        """
        Retorna estado actual de la conexión
        
        Returns:
            dict: {'conectado': bool, 'ultima_verificacion': datetime}
        """
        return {
            'conectado': self.conectado,
            'ultima_verificacion': self.ultima_verificacion
        }
