import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api"     

def _convertir_fechas_respuesta(data):
    """
    Convierte TODAS las fechas ISO-8601 a YYYY-MM-DD
    """
    if isinstance(data, dict):
        for clave, valor in data.items():
            # Si es una fecha (termina en 'fecha' o contiene 'date')
            if isinstance(valor, str) and ('fecha' in clave.lower() or 'date' in clave.lower()):
                # Si está en formato ISO-8601 (contiene 'T')
                if 'T' in valor and 'Z' in valor:
                    try:
                        # Convertir 2025-12-03T00:00:00Z → 2025-12-03
                        fecha_obj = datetime.fromisoformat(valor.replace('Z', '+00:00'))
                        data[clave] = fecha_obj.strftime('%Y-%m-%d')
                    except:
                        pass  # Si falla, dejar como estaba
    elif isinstance(data, list):
        for item in data:
            _convertir_fechas_respuesta(item)  # Recursivo para listas
    
    return data

# -------- Helper para manejar errores HTTP -------- #
def _hacer_request(metodo, endpoint, json_data=None):
    """
    Realiza una solicitud HTTP y maneja errores.
    
    Args:
        metodo: 'GET', 'POST', 'PUT', 'DELETE'
        endpoint: URL completa
        json_data: datos para POST/PUT
    
    Returns:
        dict con respuesta (json) o error
    """
    try:
        print(f"[DEBUG] {metodo} {endpoint}")
        if json_data:
            print(f"[DEBUG] Data enviada: {json_data}")
        
        if metodo == 'GET':
            resp = requests.get(endpoint, timeout=5)
        elif metodo == 'POST':
            resp = requests.post(endpoint, json=json_data, timeout=5)
        elif metodo == 'PUT':
            resp = requests.put(endpoint, json=json_data, timeout=5)
        elif metodo == 'DELETE':
            resp = requests.delete(endpoint, timeout=5)
        else:
            return {"error": f"Método no soportado: {metodo}"}
        
        print(f"[DEBUG] Status: {resp.status_code}")
        
        # Verificar status HTTP
        if resp.status_code >= 400:
            print(f"[ERROR] {resp.status_code}: {resp.text}")
            try:
                error_data = resp.json()
                print(f"[ERROR] Response: {error_data}")
                return error_data
            except:
                return {"error": f"HTTP {resp.status_code}: {resp.text}"}
        
        # Retornar respuesta
        if metodo == 'DELETE':
            print(f"[SUCCESS] Eliminado correctamente")
            return {"status": resp.status_code}
        
        respuesta = resp.json()
        print(f"[SUCCESS] Response: {respuesta}")
        
        # ✅ Convertir fechas ISO-8601 a YYYY-MM-DD
        if metodo == 'GET':
            respuesta = _convertir_fechas_respuesta(respuesta)
        elif metodo in ['POST', 'PUT']:
            # También convertir en POST/PUT para mostrar datos actualizados
            respuesta = _convertir_fechas_respuesta(respuesta)
        
        return respuesta
    
    except requests.exceptions.Timeout:
        error_msg = "Timeout: El servidor no responde"
        print(f"[ERROR] {error_msg}")
        return {"error": error_msg}
    except requests.exceptions.ConnectionError:
        error_msg = "Error de conexión: No se puede conectar al servidor"
        print(f"[ERROR] {error_msg}")
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return {"error": error_msg}

# ---------------- Herramientas ---------------- #

def obtener_herramientas():
    return _hacer_request('GET', f"{API_URL}/herramientas/")

def crear_herramienta(data):
    return _hacer_request('POST', f"{API_URL}/herramientas/", data)

def actualizar_herramienta(codigo, data):
    """Actualiza herramienta usando 'codigo' como lookup"""
    return _hacer_request('PUT', f"{API_URL}/herramientas/{codigo}/", data)

def eliminar_herramienta(codigo):
    """Elimina herramienta usando 'codigo' como lookup"""
    return _hacer_request('DELETE', f"{API_URL}/herramientas/{codigo}/")


# ---------------- Préstamos ---------------- #

def obtener_prestamos():
    return _hacer_request('GET', f"{API_URL}/prestamos/")

def crear_prestamo(data):
    return _hacer_request('POST', f"{API_URL}/prestamos/", data)

def actualizar_prestamo(numero, data):
    """Actualiza préstamo usando 'numero' como lookup"""
    return _hacer_request('PUT', f"{API_URL}/prestamos/{numero}/", data)

def eliminar_prestamo(numero):
    """Elimina préstamo usando 'numero' como lookup"""
    return _hacer_request('DELETE', f"{API_URL}/prestamos/{numero}/")
