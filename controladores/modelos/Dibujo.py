import tkinter as tk

class Dibujo():
    def __init__(self, root):
        self.root = root
        self.var_valor = tk.StringVar()
        self.var_tipo_Dibujo = tk.StringVar()
        self.var_fecha_Realizacion = tk.StringVar()
        self.var_Autor = tk.StringVar()
