import tkinter as tk
import re
from tkinter.messagebox import askyesno, showerror, showinfo
from datetime import datetime

root = tk.Tk()
root.title("Dibujo")
root.geometry("420x380")
root.resizable(0,0)
root.config(padx=20, pady=20)

def el_usuario_quiere_salir():
    if askyesno("Salir de la aplicacion", "Estas seguro de quieres cerrar la aplicacion"):
        root.destroy()

val_valor = re.compile(r"^[0-9.]*$")
val_tipo_Dibujo = re.compile(r"^[A-Za-z .]*$")



def limpiar_campos_texto():
    for var, err in [
        (var_valor, err_valor),
        (var_tipo_Dibujo, err_tipo_Dibujo),
        (var_fecha_Realizacion, err_fecha_Realizacion),
        (var_Autor, err_Autor)
    ]:
        var.set("")
        err.set("")

import re
from tkinter import messagebox

def val_valor():
    txt = entry_valor.get()
    patron = r"^\d{1,5}$"  
    if re.match(patron, txt):
        print("Valor válido")
        entry_valor.config(bg="white")
        return True
    else:
        print("Valor inválido")
        entry_valor.config(bg="red")
        return False

def val_tipo_Dibujo():
    txt = entry_tipo_Dibujo.get()
    patron = r"^[A-Za-z\s]+$"  
    if re.match(patron, txt):
        print("Tipo de dibujo válido")
        entry_tipo_Dibujo.config(bg="white")
        return True
    else:
        print("Tipo de dibujo inválido")
        entry_tipo_Dibujo.config(bg="red")
        return False

def val_fecha_Realizacion():
    txt = entry_fecha_Realizacion.get()
    patron = r"^\d{4}-\d{2}-\d{2}$"  
    if re.match(patron, txt):
        print("Fecha válida")
        entry_fecha_Realizacion.config(bg="white")
        return True
    else:
        print("Fecha inválida")
        entry_fecha_Realizacion.config(bg="red")
        return False

def val_Autor():
    txt = entry_Autor.get()
    patron = r"^[A-Za-z\s]+$"
    if re.match(patron, txt):
        print("Autor válido")
        entry_Autor.config(bg="white")
        return True
    else:
        print("Autor inválido")
        entry_Autor.config(bg="red")
        return False


def enviar():
    ok = all([
        val_valor(),
        val_tipo_Dibujo(),
        val_fecha_Realizacion(),
        val_Autor(),
    ])
    obligatorios = [
        (var_valor.get().strip() != "", err_valor, "La versión es obligatoria."),
        (var_tipo_Dibujo.get().strip() != "", err_tipo_Dibujo, "El tipo es obligatorio."),
        (var_fecha_Realizacion.get().strip() != "", err_fecha_Realizacion, "La fecha de publicación es obligatoria."),
        (var_Autor.get().strip() != "", err_Autor, "El firewall es obligatorio."),
    ]
    for lleno, err_var, msg in obligatorios:
        if not lleno and err_var.get() == "":
            err_var.set(msg)
            ok = False

    if not ok:
        showerror("Errores de validación", "Por favor complete los campos marcados en rojo.")
        return

    showinfo("OK", "Formulario válido. ¡Datos guardados!")

# Variables de entrada
var_valor = tk.StringVar()
var_tipo_Dibujo = tk.StringVar()
var_fecha_Realizacion = tk.StringVar()
var_Autor = tk.StringVar()

# Variables de error
err_valor = tk.StringVar()
err_tipo_Dibujo = tk.StringVar()
err_fecha_Realizacion = tk.StringVar()
err_Autor = tk.StringVar()

# Etiquetas y campos
label_opts = dict(sticky="e", padx=(0,10), pady=(0,8))
entry_opts = dict(sticky="w", padx=(0,10), pady=(0,8))

tk.Label(root, text="Valor").grid(row=0, column=0, **label_opts)
entry_valor = tk.Entry(root, textvariable=var_valor, width=25)
entry_valor.grid(row=0, column=1, **entry_opts)
tk.Label(root, textvariable=err_valor, fg="#d83c8a").grid(row=1, column=1, sticky="w", pady=(0,8))

tk.Label(root, text="Tipo Dibujo").grid(row=2, column=0, **label_opts)
entry_tipo_Dibujo = tk.Entry(root, textvariable=var_tipo_Dibujo, width=25)
entry_tipo_Dibujo.grid(row=2, column=1, **entry_opts)
tk.Label(root, textvariable=err_tipo_Dibujo, fg="#d83c8a").grid(row=3, column=1, sticky="w", pady=(0,8))

tk.Label(root, text="Fecha de Realizacion").grid(row=4, column=0, **label_opts)
entry_fecha_Realizacion= tk.Entry(root, textvariable=var_fecha_Realizacion, width=25)
entry_fecha_Realizacion.grid(row=4, column=1, **entry_opts)
tk.Label(root, textvariable=err_fecha_Realizacion, fg="#d83c8a").grid(row=5, column=1, sticky="w", pady=(0,8))

tk.Label(root, text="Autor").grid(row=6, column=0, **label_opts)
entry_Autor = tk.Entry(root, textvariable=var_Autor, width=25)
entry_Autor.grid(row=6, column=1, **entry_opts)
tk.Label(root, textvariable=err_Autor, fg="#d83c8a").grid(row=7, column=1, sticky="w", pady=(0,8))

# Frame para los botones
boton_frame = tk.Frame(root)
boton_frame.grid(row=8, column=0, columnspan=2, pady=(18,0))

tk.Button(boton_frame, text="Validar Información", command=enviar, width=18).pack(side="left", padx=10)
tk.Button(boton_frame, text="Limpiar", command=limpiar_campos_texto, width=12).pack(side="left", padx=10)

# Eventos de validación en vivo
entry_valor.bind("<KeyRelease>", lambda e: val_valor())
entry_tipo_Dibujo.bind("<KeyRelease>", lambda e: val_tipo_Dibujo())
entry_fecha_Realizacion.bind("<KeyRelease>", lambda e: val_fecha_Realizacion())
entry_Autor.bind("<KeyRelease>", lambda e: val_Autor())

root.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)
root.mainloop()