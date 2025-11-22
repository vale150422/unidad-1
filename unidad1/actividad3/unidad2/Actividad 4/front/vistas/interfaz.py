import tkinter as tk
from controladores.comunicacion import Comunicacion
from modelos.usuario import Usuario
from .tabla import Tabla

class Interfaz():

    def __init__(self):
        titulos = ['Identificador', 'Tema', 'Descripción', 'Número de clase']
        columnas = ['id', 'tema', 'descripcion', 'numero_clase']
        data = []
        self.ventanaPrincipal = tk.Tk()
        self.comunicacion = Comunicacion(self.ventanaPrincipal)
        self.tabla = Tabla(self.ventanaPrincipal, titulos, columnas, data)
        pass

    def accion_guardar_boton(self, id, tema, descripcion, numero):
        if id == '':
            self.comunicacion.guardar(tema, descripcion, numero)
        else:
            self.comunicacion.actualizar(id, tema, descripcion, numero)

    def accion_consultar_boton(self, labelConsulta, id):
        resultado = self.comunicacion.consultar(id)
        labelConsulta.config(text = resultado.get('numero_clase'))

    def accion_consultar_todo(self, tema, descripcion, numero):
        resultado = self.comunicacion.consultar_todo(tema, descripcion, numero)
        data = []
        for elemento in resultado:
            data.append((elemento.get('id'), elemento.get('tema'), elemento.get('descripcion'), elemento.get('numero_clase')))
        self.tabla.refrescar(data)
        print(data)

    def mostrar_interfaz(self):
        usuario = Usuario(self.ventanaPrincipal)

        labelId = tk.Label(self.ventanaPrincipal, text="Id")
        entryId = tk.Entry(self.ventanaPrincipal, textvariable=usuario.id)
        labelTema = tk.Label(self.ventanaPrincipal, text="Tema")
        entryTema = tk.Entry(self.ventanaPrincipal, textvariable=usuario.tema)
        labelDescripcion = tk.Label(self.ventanaPrincipal, text="Descripcion")
        entryDescripcion = tk.Entry(self.ventanaPrincipal, textvariable=usuario.descripcion)
        labelNumero = tk.Label(self.ventanaPrincipal, text="Número de clase")
        entryNumero = tk.Entry(self.ventanaPrincipal, textvariable=usuario.numero_clase)
        labelConsulta = tk.Label(self.ventanaPrincipal, text='')
        
        boton_guardar = tk.Button(self.ventanaPrincipal, 
                   text="Guardar", 
                   command=lambda: self.accion_guardar_boton(entryId.get(), entryTema.get(), entryDescripcion.get(), entryNumero.get()))
        
        boton_consultar_1 = tk.Button(self.ventanaPrincipal, 
                   text="Consultar 1", 
                   command=lambda: self.accion_consultar_boton(labelConsulta, entryNumero.get()))
        
        boton_consultar_todos = tk.Button(self.ventanaPrincipal, 
                   text="Consultar todos", 
                   command=lambda: self.accion_consultar_todo(entryTema.get(), entryDescripcion.get(), entryNumero.get()))

        #creando la ventana
        self.ventanaPrincipal.title("Ventana Principal")
        self.ventanaPrincipal.geometry("1000x1000")
        labelId.pack()
        entryId.pack()
        labelTema.pack()
        entryTema.pack()
        labelDescripcion.pack()
        entryDescripcion.pack()
        labelNumero.pack()
        entryNumero.pack()
        boton_guardar.pack()
        boton_consultar_1.pack()
        boton_consultar_todos.pack()
        labelConsulta.pack()
        self.tabla.tabla.pack()

        def seleccionar_elemento(_):
            for i in self.tabla.tabla.selection():
                valores = self.tabla.tabla.item(i)['values']
                entryId.delete(0, tk.END)
                entryId.insert(0, str(valores[0]))
                entryTema.delete(0, tk.END)
                entryTema.insert(0, str(valores[1]))
                entryDescripcion.delete(0, tk.END)
                entryDescripcion.insert(0, str(valores[2]))
                entryNumero.delete(0, tk.END)
                entryNumero.insert(0, str(valores[3]))

        def borrar_elemento(_):
            for i in self.tabla.tabla.selection():
                self.comunicacion.eliminar(self.tabla.tabla.item(i)['values'][0])
                self.tabla.tabla.delete(i)

        self.tabla.tabla.bind('<<TreeviewSelect>>', seleccionar_elemento)
        self.tabla.tabla.bind('<Delete>', borrar_elemento)

        self.ventanaPrincipal.mainloop()