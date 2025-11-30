import requests

API_URL = "http://127.0.0.1:8000/api"     # Ajusta si usas otro puerto

# ---------------- Herramientas ---------------- #

def obtener_herramientas():
    resp = requests.get(f"{API_URL}/herramientas/")
    return resp.json()

def crear_herramienta(data):
    resp = requests.post(f"{API_URL}/herramientas/", json=data)
    return resp.json()

def actualizar_herramienta(codigo, data):
    resp = requests.put(f"{API_URL}/herramientas/{codigo}/", json=data)
    return resp.json()

def eliminar_herramienta(codigo):
    resp = requests.delete(f"{API_URL}/herramientas/{codigo}/")
    return resp.status_code


# ---------------- Préstamos ---------------- #

def obtener_prestamos():
    resp = requests.get(f"{API_URL}/prestamos/")
    return resp.json()

def crear_prestamo(data):
    resp = requests.post(f"{API_URL}/prestamos/", json=data)
    return resp.json()

def actualizar_prestamo(numero, data):
    resp = requests.put(f"{API_URL}/prestamos/{numero}/", json=data)
    return resp.json()

def eliminar_prestamo(numero):
    resp = requests.delete(f"{API_URL}/prestamos/{numero}/")
    return resp.status_code
