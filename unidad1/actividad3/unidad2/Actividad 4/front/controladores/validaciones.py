import re

class Validaciones():
    
    def __init__(self):
        pass

    def validarLetras(valor):
        patron = re.compile("^[A-Za-zñÑ ]*$")
        resultado = patron.match(valor.get()) is not None
        if not resultado:
            return False
        return True