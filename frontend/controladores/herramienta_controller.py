"""
Controller para Herramientas
Se comunica con la API REST y coordina con la vista Tkinter
"""

from controladores.comunicacion import (
    obtener_herramientas,
    crear_herramienta as api_crear_herramienta,
    actualizar_herramienta as api_actualizar_herramienta,
    eliminar_herramienta as api_eliminar_herramienta
)
from controladores.validaciones import Validaciones


class HerramientasController:
    """Controller para operaciones CRUD de herramientas"""

    def __init__(self, view=None):
        """
        Inicializa el controller
        
        Args:
            view: Vista Tkinter (opcional)
        """
        self.view = view
        self.validaciones = Validaciones()

 
    def cargar_lista(self):
        """
        Obtiene lista de herramientas desde API
        
        Returns:
            list: Lista de herramientas o lista vacía si hay error
        """
        try:
            resultado = obtener_herramientas()
            
            # Si hay error, retornar lista vacía
            if isinstance(resultado, dict) and "error" in resultado:
                print(f"[ERROR] cargar_lista: {resultado.get('error')}")
                return []
            
            return resultado if isinstance(resultado, list) else []
        except Exception as e:
            print(f"[ERROR] cargar_lista: {e}")
            return []

    def crear(self, nombre, categoria, ubicacion, estado):
        """
        Crea nueva herramienta
        
        Args:
            nombre: Nombre de la herramienta
            categoria: Categoría
            ubicacion: Ubicación
            estado: Estado (disponible, prestada, dañada)
            
        Returns:
            dict: Respuesta de API (con 'codigo' si éxito o 'error' si falla)
        """
        print(f"[DEBUG] Crear herramienta: {nombre}")
        
        # Validar datos
        data = {
            "nombre": nombre.strip(),
            "categoria": categoria.strip(),
            "ubicacion": ubicacion.strip(),
            "estado": estado.strip()
        }
        
        errores = self.validaciones.validar_herramienta(data)
        if errores:
            print(f"[ERROR] Validación fallida: {errores}")
            return {"error": "\n".join(errores)}
        
        try:
            resultado = api_crear_herramienta(data)
            
            # Si éxito, actualizar vista
            if isinstance(resultado, dict) and "error" not in resultado:
                print(f"[SUCCESS] Herramienta creada: {resultado.get('codigo')}")
                if self.view:
                    self.view.cargar_datos_backend()
            
            return resultado
        except Exception as e:
            print(f"[ERROR] crear: {e}")
            return {"error": str(e)}

    def actualizar(self, codigo, nombre, categoria, ubicacion, estado):
        """
        Actualiza herramienta existente
        
        Args:
            codigo: Código de la herramienta
            nombre: Nuevo nombre
            categoria: Nueva categoría
            ubicacion: Nueva ubicación
            estado: Nuevo estado
            
        Returns:
            dict: Respuesta de API
        """
        print(f"[DEBUG] Actualizar herramienta: {codigo}")
        
        if not codigo or codigo.strip() == "":
            return {"error": "Código requerido"}
        
        # Validar datos
        data = {
            "nombre": nombre.strip(),
            "categoria": categoria.strip(),
            "ubicacion": ubicacion.strip(),
            "estado": estado.strip()
        }
        
        errores = self.validaciones.validar_herramienta(data)
        if errores:
            print(f"[ERROR] Validación fallida: {errores}")
            return {"error": "\n".join(errores)}
        
        try:
            resultado = api_actualizar_herramienta(codigo, data)
            
            # Si éxito, actualizar vista
            if isinstance(resultado, dict) and "error" not in resultado:
                print(f"[SUCCESS] Herramienta actualizada: {codigo}")
                if self.view:
                    self.view.cargar_datos_backend()
            
            return resultado
        except Exception as e:
            print(f"[ERROR] actualizar: {e}")
            return {"error": str(e)}

    def eliminar(self, codigo):
        """
        Elimina herramienta
        
        Args:
            codigo: Código de la herramienta a eliminar
            
        Returns:
            dict: Respuesta de API
        """
        print(f"[DEBUG] Eliminar herramienta: {codigo}")
        
        if not codigo or codigo.strip() == "":
            return {"error": "Código requerido"}
        
        try:
            resultado = api_eliminar_herramienta(codigo)
            
            # Si éxito, actualizar vista
            if not (isinstance(resultado, dict) and "error" in resultado):
                print(f"[SUCCESS] Herramienta eliminada: {codigo}")
                if self.view:
                    self.view.cargar_datos_backend()
            
            return resultado
        except Exception as e:
            print(f"[ERROR] eliminar: {e}")
            return {"error": str(e)}

    def obtener_por_codigo(self, codigo):
        """
        Obtiene herramienta específica
        
        Args:
            codigo: Código de la herramienta
            
        Returns:
            dict: Datos de la herramienta o error
        """
        try:
            lista = self.cargar_lista()
            for h in lista:
                if h.get("codigo") == codigo:
                    return h
            return {"error": "Herramienta no encontrada"}
        except Exception as e:
            print(f"[ERROR] obtener_por_codigo: {e}")
            return {"error": str(e)}


    def validar(self, nombre, categoria, ubicacion, estado):
        """
        Valida datos de herramienta
        
        Args:
            nombre: Nombre
            categoria: Categoría
            ubicacion: Ubicación
            estado: Estado
            
        Returns:
            list: Lista de errores (vacía si es válido)
        """
        data = {
            "nombre": nombre.strip(),
            "categoria": categoria.strip(),
            "ubicacion": ubicacion.strip(),
            "estado": estado.strip()
        }
        return self.validaciones.validar_herramienta(data)

    def buscar(self, termino):
        """
        Busca herramientas por nombre o categoría
        
        Args:
            termino: Término de búsqueda
            
        Returns:
            list: Herramientas que coinciden
        """
        try:
            lista = self.cargar_lista()
            termino_lower = termino.lower().strip()
            
            resultados = []
            for h in lista:
                nombre = h.get("nombre", "").lower()
                categoria = h.get("categoria", "").lower()
                codigo = h.get("codigo", "").lower()
                
                if (termino_lower in nombre or 
                    termino_lower in categoria or 
                    termino_lower in codigo):
                    resultados.append(h)
            
            return resultados
        except Exception as e:
            print(f"[ERROR] buscar: {e}")
            return []
