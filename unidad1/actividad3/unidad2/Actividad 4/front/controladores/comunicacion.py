import requests

class Comunicacion():

    def __init__(self, ventanaPrincipal):
        self.url = 'http://localhost:8000/v1/clase'
        self.ventanaPrincipal = ventanaPrincipal
        pass

    def guardar(self, tema, descripcion, numero_clase):
        try:
            print(tema, descripcion, numero_clase)
            data = {
                'tema': tema,
                'descripcion': descripcion,
                'numero_clase': int(numero_clase)
            }
            resultado = requests.post(self.url, json=data)
            print(resultado.json)
            return resultado
        except:
            pass

    def actualizar(self, id, tema, descripcion, numero_clase):
        try:
            print(tema, descripcion, numero_clase)
            data = {
                'tema': tema,
                'descripcion': descripcion,
                'numero_clase': int(numero_clase)
            }
            resultado = requests.put(self.url + '/' + str(id)+ '/', json=data)
            print(resultado.json)
            return resultado
        except:
            pass
    
    def consultar(self, id):
        resultado = requests.get(self.url + '/' + str(id))
        return resultado.json()
    
    def consultar_todo(self, titulo, descripcion, numero):
        url = self.url+ "?"
        print(type(numero))
        if numero != '':
            url = url + 'numero_clase=' + str(numero) + "&"
        if titulo != '':
            url = url + 'titulo=' + str(titulo) + "&"
        print(url)
        resultado = requests.get(url)
        return resultado.json()
    
    def eliminar(self, id):
        resultado = requests.delete(self.url + '/' + str(id))
        return resultado.status_code