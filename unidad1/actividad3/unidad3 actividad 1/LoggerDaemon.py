import threading
import time

class LoggerDaemon(threading.Thread):
    def __init__(self, intervalo):
        super().__init__(daemon=True)  
        self.intervalo = intervalo

    def run(self):
        
        while True:
            print(" [Logger] El programa sigue ejecutándose...")
            time.sleep(self.intervalo)


class TrabajoPesado(threading.Thread):
    def __init__(self, pasos):
        super().__init__()
        self.pasos = pasos

    def run(self):
        
        for i in range(1, self.pasos + 1):
            print(f" Ejecutando paso {i}/{self.pasos}...")
            time.sleep(1)  
        print(" Trabajo pesado completado.")


def main():
    
    logger = LoggerDaemon(intervalo=2)
    trabajador = TrabajoPesado(pasos=5)

    
    logger.start()
    trabajador.start()

    
    trabajador.join()

    
    print(" Programa finalizado correctamente.")


if __name__ == "__main__":
    main()
