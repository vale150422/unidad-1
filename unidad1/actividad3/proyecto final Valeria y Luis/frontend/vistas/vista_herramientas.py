from tkinter import Frame, Label, Entry, Button, StringVar
from vistas.tabla import Tabla

# ----------------------- API -----------------------
# IMPORTAMOS SOLO FUNCIONES, SIN MODIFICAR TU ESTRUCTURA
from controladores.comunicacion import (
    obtener_herramientas,
    crear_herramienta as api_crear_herramienta,
    actualizar_herramienta as api_actualizar_herramienta,
    eliminar_herramienta as api_eliminar_herramienta
)
# ---------------------------------------------------

# ✅ NO generar código automáticamente - el servidor lo hace
# Solo mostrar el código que viene del backend
# El frontend NO debe generar códigos numéricos


class VistaHerramientas(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.lista_herramientas = []
        self.fila_seleccionada = None

        Label(self, text="Gestión de Herramientas", font=("Arial", 14)).pack(pady=10)

        form_frame = Frame(self)
        form_frame.pack(pady=5)

        self.codigo_var = StringVar()
        self.nombre_var = StringVar()
        self.categoria_var = StringVar()
        self.ubicacion_var = StringVar()
        self.estado_var = StringVar()

        Label(form_frame, text="Código").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_entry = Entry(form_frame, textvariable=self.codigo_var, state="readonly")
        self.codigo_entry.grid(row=0, column=1)

        Label(form_frame, text="Nombre").grid(row=1, column=0, padx=5, pady=5)
        Entry(form_frame, textvariable=self.nombre_var).grid(row=1, column=1)

        Label(form_frame, text="Categoría").grid(row=2, column=0, padx=5, pady=5)
        Entry(form_frame, textvariable=self.categoria_var).grid(row=2, column=1)

        Label(form_frame, text="Ubicación").grid(row=3, column=0, padx=5, pady=5)
        Entry(form_frame, textvariable=self.ubicacion_var).grid(row=3, column=1)

        Label(form_frame, text="Estado").grid(row=4, column=0, padx=5, pady=5)
        Entry(form_frame, textvariable=self.estado_var).grid(row=4, column=1)

        btn_frame = Frame(self)
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Crear", width=12, command=self.crear_herramienta).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Editar", width=12, command=self.editar_herramienta).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Eliminar", width=12, command=self.eliminar_herramienta).grid(row=0, column=2, padx=5)
        Button(btn_frame, text="Limpiar", width=12, command=self.limpiar_formulario).grid(row=0, column=3, padx=5)

        columnas = ["Código", "Nombre", "Categoría", "Ubicación", "Estado"]
        self.tabla = Tabla(self, columnas)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        # CARGAR DATOS DEL BACKEND AL INICIAR
        self.cargar_datos_backend()

        # GENERAR CÓDIGO INICIAL
        self.limpiar_formulario()

    # ----------------------------- API: cargar datos -----------------------------    
    def cargar_datos_backend(self):
        """Carga herramientas desde la API y las pasa a la tabla."""
        try:
            self.lista_herramientas = obtener_herramientas()
        except:
            self.lista_herramientas = []  # Si la API falla, no rompe la UI

        self.actualizar_tabla()

    # ---------------------------------------------------------------------------

    def validar(self):
        if not self.nombre_var.get().strip():
            return "El nombre es obligatorio."
        if not self.categoria_var.get().strip():
            return "La categoría es obligatoria."
        if not self.ubicacion_var.get().strip():
            return "La ubicación es obligatoria."
        if not self.estado_var.get().strip():
            return "El estado es obligatorio."
        return None

    def crear_herramienta(self):
        from tkinter import messagebox

        error = self.validar()
        if error:
            messagebox.showerror("Error", error)
            return

        # ❌ NO ENVIAMOS 'codigo' - el servidor lo genera automáticamente
        nueva = {
            "nombre": self.nombre_var.get(),
            "categoria": self.categoria_var.get(),
            "ubicacion": self.ubicacion_var.get(),
            "estado": self.estado_var.get()
        }

        try:
            # ---------------------- API: crear ----------------------
            resp = api_crear_herramienta(nueva)
            # ---------------------------------------------------------
            
            if isinstance(resp, dict) and "error" in resp:
                messagebox.showerror("Error del servidor", resp.get("error"))
                return
            
            messagebox.showinfo("Éxito", "Herramienta creada correctamente")
            self.cargar_datos_backend()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la herramienta: {str(e)}")

    def editar_herramienta(self):
        from tkinter import messagebox

        if self.fila_seleccionada is None:
            messagebox.showerror("Error", "Seleccione un registro para editar.")
            return

        error = self.validar()
        if error:
            messagebox.showerror("Error", error)
            return

        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showerror("Error", "El código está vacío. Seleccione una fila válida.")
            return

        data = {
            "nombre": self.nombre_var.get().strip(),
            "categoria": self.categoria_var.get().strip(),
            "ubicacion": self.ubicacion_var.get().strip(),
            "estado": self.estado_var.get().strip()
        }

        print(f"[DEBUG] Editando herramienta: {codigo}")
        print(f"[DEBUG] Datos: {data}")

        try:
            # ---------------------- API: actualizar ----------------------
            resp = api_actualizar_herramienta(codigo, data)
            # ------------------------------------------------------------
            
            print(f"[DEBUG] Respuesta: {resp}")
            
            # Verificar si hubo error
            if not resp or (isinstance(resp, dict) and "error" in resp):
                error_msg = resp.get("error", "Error desconocido") if isinstance(resp, dict) else "Error desconocido"
                messagebox.showerror("Error del servidor", error_msg)
                return
            
            messagebox.showinfo("Éxito", "Herramienta actualizada correctamente")
            self.cargar_datos_backend()
            self.limpiar_formulario()
            self.fila_seleccionada = None
        except Exception as e:
            print(f"[ERROR] Exception: {str(e)}")
            messagebox.showerror("Error", f"No se pudo actualizar la herramienta: {str(e)}")


    def eliminar_herramienta(self):
        from tkinter import messagebox

        if self.fila_seleccionada is None:
            messagebox.showerror("Error", "Seleccione un registro para eliminar.")
            return

        codigo = self.lista_herramientas[self.fila_seleccionada]["codigo"]

        # ---------------------- API: eliminar ----------------------
        api_eliminar_herramienta(codigo)
        # ----------------------------------------------------------

        self.cargar_datos_backend()
        self.limpiar_formulario()
        self.fila_seleccionada = None

    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.ubicacion_var.set("")
        self.estado_var.set("")

        # ✅ El código se genera en el backend, no en el frontend
        # Solo limpiar el campo para crear nueva herramienta
        self.codigo_var.set("")

    def actualizar_tabla(self):
        self.tabla.limpiar()
        for h in self.lista_herramientas:
            self.tabla.agregar_fila((
                h["codigo"],
                h["nombre"],
                h["categoria"],
                h["ubicacion"],
                h["estado"]
            ))

    def seleccionar_fila(self, event):
        """Carga datos en el formulario cuando se selecciona una fila de la tabla"""
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        try:
            index = self.tabla.index(seleccion[0])
            if index is None:
                return
                
            self.fila_seleccionada = index
            datos = self.lista_herramientas[index]

            self.codigo_var.set(datos["codigo"])
            self.nombre_var.set(datos["nombre"])
            self.categoria_var.set(datos["categoria"])
            self.ubicacion_var.set(datos["ubicacion"])
            self.estado_var.set(datos["estado"])
        except Exception as e:
            print(f"[ERROR] seleccionar_fila: {e}")
            self.fila_seleccionada = None
