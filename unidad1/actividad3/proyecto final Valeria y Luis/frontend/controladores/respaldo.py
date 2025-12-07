"""
Módulo de respaldo automático del sistema IHEP
Realiza backups periódicos de herramientas y préstamos en formato JSON
Usa threading para no bloquear la interfaz gráfica
"""

import json
import os
import threading
import time
from datetime import datetime
from pathlib import Path
import requests


class RespaldoAutomatico:
    """
    Realiza respaldos automáticos de los datos del backend en formato JSON
    Los respaldos se guardan en una carpeta local sin intervención del usuario
    """
    
    def __init__(self, 
                 api_url="http://127.0.0.1:8000/api",
                 intervalo_segundos=None,
                 directorio_respaldo=None):
        """
        Inicializa el sistema de respaldo automático
        
        Args:
            api_url: URL base de la API (default: http://127.0.0.1:8000/api)
            intervalo_segundos: Segundos entre respaldos
                               - Si es None: lee INTERVALO_BACKUP_SEG de variables de entorno
                               - Si env var no existe: default 300 segundos (5 minutos)
            directorio_respaldo: Carpeta para guardar respaldos
                                - Si es None: crea carpeta "backups" en la raíz del proyecto
        """
        self.api_url = api_url
        
        # Configurar intervalo desde variable de entorno o parámetro
        if intervalo_segundos is None:
            env_intervalo = os.getenv("INTERVALO_BACKUP_SEG")
            self.intervalo_segundos = int(env_intervalo) if env_intervalo else 300
        else:
            self.intervalo_segundos = intervalo_segundos
        
        # Configurar directorio de respaldos
        if directorio_respaldo is None:
            # Crear carpeta "backups" en la raíz del proyecto (frontend)
            self.directorio_respaldo = Path(__file__).parent.parent.parent / "backups"
        else:
            self.directorio_respaldo = Path(directorio_respaldo)
        
        # Crear directorio si no existe
        self.directorio_respaldo.mkdir(parents=True, exist_ok=True)
        
        # Variables de control
        self.activo = False
        self.hilo = None
        self.callbacks = []  # Funciones a llamar cuando se completa un respaldo
        self.ultimo_respaldo = None
        self.cantidad_respaldos = 0
    
    def registrar_callback(self, callback):
        """
        Registra una función para ejecutar cuando se completa un respaldo
        
        Args:
            callback: Función que recibe (exitoso, timestamp, cantidad_registros)
        """
        self.callbacks.append(callback)
    
    def iniciar(self):
        """Inicia el respaldo automático en un hilo separado"""
        if self.activo:
            return
        
        self.activo = True
        self.hilo = threading.Thread(target=self._loop_respaldo, daemon=True)
        self.hilo.start()
    
    def detener(self):
        """Detiene el respaldo automático de forma segura"""
        self.activo = False
        if self.hilo:
            self.hilo.join(timeout=2)
    
    def _loop_respaldo(self):
        """Loop principal que ejecuta respaldos periódicamente"""
        while self.activo:
            try:
                self._realizar_respaldo()
            except Exception as e:
                print(f"Error en respaldo: {e}")
                # Notificar callbacks de error
                for callback in self.callbacks:
                    try:
                        callback(False, datetime.now(), 0, str(e))
                    except:
                        pass
            
            # Esperar el intervalo configurado
            time.sleep(self.intervalo_segundos)
    
    def _realizar_respaldo(self):
        """
        Obtiene datos del backend y guarda en archivo JSON local
        """
        try:
            # Obtener datos del backend
            herramientas_resp = requests.get(
                f"{self.api_url}/herramientas/",
                timeout=5
            )
            prestamos_resp = requests.get(
                f"{self.api_url}/prestamos/",
                timeout=5
            )
            
            herramientas_resp.raise_for_status()
            prestamos_resp.raise_for_status()
            
            datos_herramientas = herramientas_resp.json()
            datos_prestamos = prestamos_resp.json()
            
            # Preparar estructura de respaldo
            respaldo = {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "herramientas": datos_herramientas if isinstance(datos_herramientas, list) else [],
                "prestamos": datos_prestamos if isinstance(datos_prestamos, list) else [],
                "estadisticas": {
                    "total_herramientas": len(datos_herramientas) if isinstance(datos_herramientas, list) else 0,
                    "total_prestamos": len(datos_prestamos) if isinstance(datos_prestamos, list) else 0
                }
            }
            
            # Generar nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"respaldo_{timestamp}.json"
            ruta_archivo = self.directorio_respaldo / nombre_archivo
            
            # Guardar archivo
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(respaldo, f, indent=2, ensure_ascii=False)
            
            # Actualizar estado
            self.ultimo_respaldo = datetime.now()
            self.cantidad_respaldos += 1
            
            # Limpiar respaldos antiguos (mantener solo los últimos 10)
            self._limpiar_respaldos_antiguos(max_respaldos=10)
            
            # Notificar callbacks de éxito
            total_registros = respaldo["estadisticas"]["total_herramientas"] + respaldo["estadisticas"]["total_prestamos"]
            for callback in self.callbacks:
                try:
                    callback(True, self.ultimo_respaldo, total_registros)
                except:
                    pass
        
        except Exception as e:
            raise Exception(f"No se pudo conectar con el backend: {str(e)}")
    
    def _limpiar_respaldos_antiguos(self, max_respaldos=10):
        """
        Mantiene solo los respaldos más recientes y elimina los antiguos
        
        Args:
            max_respaldos: Cantidad máxima de respaldos a mantener
        """
        try:
            archivos = sorted(
                self.directorio_respaldo.glob("respaldo_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Eliminar archivos antiguos
            for archivo in archivos[max_respaldos:]:
                archivo.unlink()
        except:
            pass  # Si hay error al limpiar, continuamos sin problema
    
    def obtener_estado(self):
        """
        Retorna información del estado del respaldo
        
        Returns:
            dict con: {
                'activo': bool,
                'intervalo': int (segundos),
                'ultimo_respaldo': datetime o None,
                'cantidad_respaldos': int,
                'directorio': str,
                'proxima_verificacion': int (segundos hasta próximo respaldo)
            }
        """
        tiempo_desde_ultimo = None
        proxima_en = self.intervalo_segundos
        
        if self.ultimo_respaldo:
            tiempo_transcurrido = (datetime.now() - self.ultimo_respaldo).total_seconds()
            tiempo_desde_ultimo = int(tiempo_transcurrido)
            proxima_en = max(0, self.intervalo_segundos - tiempo_transcurrido)
        
        return {
            'activo': self.activo,
            'intervalo': self.intervalo_segundos,
            'ultimo_respaldo': self.ultimo_respaldo,
            'tiempo_desde_ultimo': tiempo_desde_ultimo,
            'cantidad_respaldos': self.cantidad_respaldos,
            'directorio': str(self.directorio_respaldo),
            'proxima_verificacion': int(proxima_en)
        }
    
    def listar_respaldos(self):
        """
        Retorna lista de archivos de respaldo existentes
        
        Returns:
            list de dict con: {'nombre': str, 'fecha': datetime, 'tamaño': int}
        """
        respaldos = []
        try:
            for archivo in sorted(
                self.directorio_respaldo.glob("respaldo_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            ):
                respaldos.append({
                    'nombre': archivo.name,
                    'fecha': datetime.fromtimestamp(archivo.stat().st_mtime),
                    'tamaño': archivo.stat().st_size,
                    'ruta': str(archivo)
                })
        except:
            pass
        
        return respaldos
    
    def cargar_respaldo(self, nombre_archivo):
        """
        Carga un archivo de respaldo existente
        
        Args:
            nombre_archivo: Nombre del archivo (ej: respaldo_20250103_120000.json)
        
        Returns:
            dict con los datos del respaldo o None si hay error
        """
        try:
            ruta = self.directorio_respaldo / nombre_archivo
            
            if not ruta.exists():
                return None
            
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
