import requests

class ClienteAPI:
    def __init__(self, url_base="http://127.0.0.1:8000/"):
        self.url_base = url_base

    def consultar_prestamos(self):
        url = self.url_base + "prestamos/"
        respuesta = requests.get(url)
        return respuesta.json()

    def crear_prestamo(self, datos):
        url = self.url_base + "prestamos/"
        respuesta = requests.post(url, json=datos)
        return respuesta.json()

    def actualizar_prestamo(self, id_prestamo, datos):
        url = self.url_base + f"prestamos/{id_prestamo}/"
        respuesta = requests.put(url, json=datos)
        return respuesta.json()

    def eliminar_prestamo(self, id_prestamo):
        url = self.url_base + f"prestamos/{id_prestamo}/"
        respuesta = requests.delete(url)
        return respuesta.status_code
