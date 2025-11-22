import threading
import time

def tarea(nombre, duracion):
    
    print(f" Iniciando tarea {nombre}...")
    
    time.sleep(duracion)
    
    print(f" Tarea {nombre} finalizada (duración: {duracion} segundos)")

def main():
    
    hilo1 = threading.Thread(target=tarea, args=("A", 1.2))
    hilo2 = threading.Thread(target=tarea, args=("B", 0.8))
    hilo3 = threading.Thread(target=tarea, args=("C", 1.5))

    
    hilo1.start()
    hilo2.start()
    hilo3.start()

    
    hilo1.join()
    hilo2.join()
    hilo3.join()

    
    print(" Terminado")

if __name__ == "__main__":
    main()

