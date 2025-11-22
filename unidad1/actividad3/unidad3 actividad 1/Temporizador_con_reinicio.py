import threading
import time

class Temporizador(threading.Thread):
    def __init__(self, limite, reset_event, stop_event):
        super().__init__()
        self.limite = limite
        self.reset_event = reset_event
        self.stop_event = stop_event

    def run(self):
        contador = 0
        while not self.stop_event.is_set():
            
            time.sleep(1)
            contador += 1
            print(f" Tiempo: {contador} segundos")

            
            if self.reset_event.is_set():
                print(" Temporizador reiniciado.")
                contador = 0
                self.reset_event.clear()

            
            if contador >= self.limite:
                print(" ¡Tiempo límite alcanzado!")
                self.stop_event.set()
                break


class EscuchaReset(threading.Thread):
    def __init__(self, reset_event):
        super().__init__(daemon=True)
        self.reset_event = reset_event

    def run(self):
        
        while True:
            input("Presiona ENTER para reiniciar el temporizador...\n")
            self.reset_event.set()


def main():
    
    reset_event = threading.Event()
    stop_event = threading.Event()

    
    temporizador = Temporizador(limite=10, reset_event=reset_event, stop_event=stop_event)
    escucha = EscuchaReset(reset_event=reset_event)

    
    escucha.start()
    temporizador.start()

    
    temporizador.join()
    print(" Programa finalizado.")


if __name__ == "__main__":
    main()










