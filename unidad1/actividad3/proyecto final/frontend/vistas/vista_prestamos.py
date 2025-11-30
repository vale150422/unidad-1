from tkinter import Frame, Label, Entry, Button, StringVar, messagebox
from vistas.tabla import Tabla
from controladores.validaciones import Validaciones

# ----------------------- API -----------------------
from controladores.comunicacion import (
    obtener_prestamos,
    crear_prestamo as api_crear_prestamo,
    actualizar_prestamo as api_actualizar_prestamo,
    eliminar_prestamo as api_eliminar_prestamo
)
# ---------------------------------------------------

# -----------------------
# GENERADOR AUTOMÁTICO
# -----------------------
def generar_codigo_auto(lista):
    if not lista:
        return "001"

    numeros = []
    for item in lista:
        try:
            numeros.append(int(item["numero"]))
        except:
            pass

    if not numeros:
        return "001"

    return f"{max(numeros)+1:03d}"


class VistaPrestamos(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.validar = Validaciones()

        self.lista_prestamos = []
        self.fila_seleccionada = None

        Label(self, text="Gestión de Préstamos", font=("Arial", 14)).pack(pady=10)

        form_frame = Frame(self)
        form_frame.pack(pady=5)

        self.numero_var = StringVar()
        self.herr_codigo_var = StringVar()
        self.responsable_var = StringVar()
        self.fecha_salida_var = StringVar()
        self.fecha_esperada_var = StringVar()
        self.fecha_devolucion_var = StringVar()

        Label(form_frame, text="Número").grid(row=0, column=0)
        self.numero_entry = Entry(form_frame, textvariable=self.numero_var, state="readonly")
        self.numero_entry.grid(row=0, column=1)

        Label(form_frame, text="Código herramienta").grid(row=0, column=2)
        Entry(form_frame, textvariable=self.herr_codigo_var).grid(row=0, column=3)

        Label(form_frame, text="Responsable").grid(row=1, column=0)
        Entry(form_frame, textvariable=self.responsable_var).grid(row=1, column=1)

        Label(form_frame, text="Fecha salida (YYYY-MM-DD)").grid(row=1, column=2)
        Entry(form_frame, textvariable=self.fecha_salida_var).grid(row=1, column=3)

        Label(form_frame, text="Fecha esperada (YYYY-MM-DD)").grid(row=2, column=0)
        Entry(form_frame, textvariable=self.fecha_esperada_var).grid(row=2, column=1)

        Label(form_frame, text="Fecha devolución (YYYY-MM-DD)").grid(row=2, column=2)
        Entry(form_frame, textvariable=self.fecha_devolucion_var).grid(row=2, column=3)

        btn_frame = Frame(self)
        btn_frame.pack(pady=8)

        Button(btn_frame, text="Crear", width=12, command=self.crear_prestamo).grid(row=0, column=0)
        Button(btn_frame, text="Editar", width=12, command=self.editar_prestamo).grid(row=0, column=1)
        Button(btn_frame, text="Eliminar", width=12, command=self.eliminar_prestamo).grid(row=0, column=2)
        Button(btn_frame, text="Limpiar", width=12, command=self.limpiar_formulario).grid(row=0, column=3)

        columnas = [
            "Número", "Herramienta", "Responsable",
            "Fecha salida", "Fecha esperada", "Fecha devolución",
        ]
        self.tabla = Tabla(self, columnas)
        self.tabla.pack(pady=10)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        # -------- API: cargar datos iniciales --------
        self.cargar_datos_backend()
        # ---------------------------------------------

        # GENERAR AL INICIAR
        self.limpiar_formulario()

    # ========================
    # CARGA DESDE BACKEND
    # ========================
    def cargar_datos_backend(self):
        try:
            self.lista_prestamos = obtener_prestamos()
        except:
            self.lista_prestamos = []

        self.actualizar_tabla()

    # ========================
    # CRUD
    # ========================
    def crear_prestamo(self):
        datos = self._leer_formulario()
        errores = self.validar.validar_prestamo(datos)

        if errores:
            messagebox.showerror("Errores de validación", "\n".join(errores))
            return

        # -------- API: crear --------
        api_crear_prestamo(datos)
        # ----------------------------

        self.cargar_datos_backend()
        self.limpiar_formulario()

    def editar_prestamo(self):
        if self.fila_seleccionada is None:
            messagebox.showwarning("Atención", "Seleccione una fila para editar.")
            return

        datos = self._leer_formulario()
        errores = self.validar.validar_prestamo(datos)

        if errores:
            messagebox.showerror("Errores", "\n".join(errores))
            return

        numero = self.numero_var.get()

        # -------- API: actualizar --------
        api_actualizar_prestamo(numero, datos)
        # ---------------------------------

        self.cargar_datos_backend()
        self.limpiar_formulario()
        self.fila_seleccionada = None

    def eliminar_prestamo(self):
        if self.fila_seleccionada is None:
            messagebox.showwarning("Atención", "Seleccione una fila para eliminar.")
            return

        numero = self.lista_prestamos[self.fila_seleccionada]["numero"]

        # -------- API: eliminar --------
        api_eliminar_prestamo(numero)
        # -------------------------------

        self.cargar_datos_backend()
        self.limpiar_formulario()
        self.fila_seleccionada = None

    # ========================
    # OTROS
    # ========================
    def limpiar_formulario(self):
        self.herr_codigo_var.set("")
        self.responsable_var.set("")
        self.fecha_salida_var.set("")
        self.fecha_esperada_var.set("")
        self.fecha_devolucion_var.set("")

        # Nuevo número automático basado en lista del backend
        nuevo = generar_codigo_auto(self.lista_prestamos)
        self.numero_var.set(nuevo)

    def _leer_formulario(self):
        return {
            "numero": self.numero_var.get().strip(),
            "herramienta_codigo": self.herr_codigo_var.get().strip(),
            "responsable": self.responsable_var.get().strip(),
            "fecha_salida": self.fecha_salida_var.get().strip(),
            "fecha_esperada": self.fecha_esperada_var.get().strip(),
            "fecha_devolucion": self.fecha_devolucion_var.get().strip(),
        }

    def actualizar_tabla(self):
        self.tabla.limpiar()
        for p in self.lista_prestamos:
            self.tabla.agregar_fila((
                p["numero"],
                p["herramienta_codigo"],
                p["responsable"],
                p["fecha_salida"],
                p["fecha_esperada"],
                p["fecha_devolucion"],
            ))

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        index = self.tabla.index(seleccion[0])
        self.fila_seleccionada = index

        datos = self.lista_prestamos[index]

        self.numero_var.set(datos["numero"])
        self.herr_codigo_var.set(datos["herramienta_codigo"])
        self.responsable_var.set(datos["responsable"])
        self.fecha_salida_var.set(datos["fecha_salida"])
        self.fecha_esperada_var.set(datos["fecha_esperada"])
        self.fecha_devolucion_var.set(datos["fecha_devolucion"])

    def obtener_filas(self):
        return self.lista_prestamos
