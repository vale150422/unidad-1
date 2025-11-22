import threading
import random
import time

class Cuenta:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial
        self.lock = threading.Lock()

    def depositar(self, monto):
        
        with self.lock:
            saldo_anterior = self.saldo
            time.sleep(0.1)  
            self.saldo += monto
            print(f" Depósito de {monto:.2f} | Saldo: {saldo_anterior:.2f} → {self.saldo:.2f}")

    def retirar(self, monto):
        
        with self.lock:
            if self.saldo >= monto:
                saldo_anterior = self.saldo
                time.sleep(0.1)  
                self.saldo -= monto
                print(f" Retiro de {monto:.2f} | Saldo: {saldo_anterior:.2f} → {self.saldo:.2f}")
            else:
                print(f" Fondos insuficientes para retirar {monto:.2f} | Saldo actual: {self.saldo:.2f}")

class OperadorCuenta(threading.Thread):
    def __init__(self, cuenta, operaciones):
        super().__init__()
        self.cuenta = cuenta
        self.operaciones = operaciones

    def run(self):
        for _ in range(self.operaciones):
            monto = random.uniform(10, 100)  
            if random.choice([True, False]):
                self.cuenta.depositar(monto)
            else:
                self.cuenta.retirar(monto)
            time.sleep(random.uniform(0.1, 0.3))  

def main():
    cuenta = Cuenta(saldo_inicial=500)  
    hilos = []

   
    for i in range(3):
        hilo = OperadorCuenta(cuenta, operaciones=5)
        hilos.append(hilo)
        hilo.start()

    
    for hilo in hilos:
        hilo.join()

    
    print(f"\n Saldo final en la cuenta: {cuenta.saldo:.2f}")

if __name__ == "__main__":
    main()
