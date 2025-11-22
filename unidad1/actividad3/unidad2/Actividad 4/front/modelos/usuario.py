import tkinter as tk

class Usuario():
        
    def __init__(self, ventanaPrincipal):
        self.ventanaPrincipal = ventanaPrincipal
        self.id = tk.StringVar(ventanaPrincipal)
        self.tema = tk.StringVar(ventanaPrincipal)
        self.descripcion = tk.StringVar(ventanaPrincipal)
        self.numero_clase = tk.StringVar(ventanaPrincipal)