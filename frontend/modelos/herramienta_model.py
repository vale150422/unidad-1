import requests

class HerramientasModel:
    BASE = "http://127.0.0.1:8000/api/herramientas/"

    @staticmethod
    def obtener_todas():
        r = requests.get(HerramientasModel.BASE)
        return r.json()

    @staticmethod
    def crear(nombre, estado):
        data = {"nombre": nombre, "estado": estado}
        r = requests.post(HerramientasModel.BASE, json=data)
        return r.status_code == 201

    @staticmethod
    def eliminar(id_h):
        r = requests.delete(f"{HerramientasModel.BASE}{id_h}/")
        return r.status_code == 204
