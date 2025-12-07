from tkinter import Frame, Label, Entry, Button, StringVar, messagebox
from vistas.tabla import Tabla
from controladores.validaciones import Validaciones
from datetime import datetime

# ----------------------- API -----------------------
from controladores.comunicacion import (
    obtener_prestamos,
    crear_prestamo as api_crear_prestamo,
    actualizar_prestamo as api_actualizar_prestamo,
    eliminar_prestamo as api_eliminar_prestamo
)
# ---------------------------------------------------

# ✅ NO generar número automáticamente - el servidor lo hace
# Solo mostrar el número que viene del backend
# El frontend NO debe generar números


def convertir_fecha_a_iso(fecha_str):
    """
    Convierte fecha de formato YYYY-MM-DD a ISO 8601 con hora
    Entrada: "2025-12-03"
    Salida: "2025-12-03T00:00:00Z"
    
    Retorna None si la fecha está vacía
    """
    if not fecha_str or fecha_str.strip() == "":
        return None
    
    fecha_limpia = fecha_str.strip()
    
    # Si ya está en formato ISO 8601, devolverlo como está
    if "T" in fecha_limpia and "Z" in fecha_limpia:
        return fecha_limpia
    
    try:
        # Parsear en formato YYYY-MM-DD
        fecha = datetime.strptime(fecha_limpia, "%Y-%m-%d")
        # Convertir a ISO 8601 con hora (00:00:00Z)
        return fecha.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        # Si falla la conversión, retornar None (el validador lo detectará)
        return None


def convertir_fecha_desde_iso(fecha_iso):
    """
    Convierte fecha ISO 8601 a formato legible YYYY-MM-DD
    Entrada: "2025-12-03T00:00:00Z"
    Salida: "2025-12-03"
    
    Si la fecha está vacía o es None, retorna vacío
    """
    if not fecha_iso or fecha_iso.strip() == "":
        return ""
    
    fecha_limpia = fecha_iso.strip()
    
    # Si ya está en formato YYYY-MM-DD, devolverlo como está
    if "T" not in fecha_limpia:
        return fecha_limpia
    
    try:
        # Parsear ISO 8601
        fecha = datetime.fromisoformat(fecha_limpia.replace("Z", "+00:00"))
        # Convertir a YYYY-MM-DD
        return fecha.strftime("%Y-%m-%d")
    except:
        # Si falla, retornar como está
        return fecha_limpia


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

        try:
            # -------- API: crear --------
            respuesta = api_crear_prestamo(datos)
            # ----------------------------
            
            # Si la API retorna errores, mostrarlos
            if isinstance(respuesta, dict) and "error" in respuesta:
                messagebox.showerror("Error del servidor", respuesta.get("error"))
                return
            
            messagebox.showinfo("Éxito", "Préstamo creado correctamente")
            self.cargar_datos_backend()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el préstamo: {str(e)}")

    def editar_prestamo(self):
        """Actualiza un préstamo existente"""
        if self.fila_seleccionada is None:
            messagebox.showwarning("Atención", "Seleccione una fila para editar.")
            return

        datos = self._leer_formulario()
        errores = self.validar.validar_prestamo(datos)

        if errores:
            messagebox.showerror("Errores", "\n".join(errores))
            return

        numero = self.numero_var.get().strip()
        if not numero:
            messagebox.showerror("Error", "El número está vacío. Seleccione una fila válida.")
            return

        print(f"[DEBUG] Editando préstamo: {numero}")
        print(f"[DEBUG] Datos: {datos}")

        try:
            # -------- API: actualizar --------
            respuesta = api_actualizar_prestamo(numero, datos)
            # ---------------------------------
            
            print(f"[DEBUG] Respuesta: {respuesta}")
            
            # Si la API retorna errores, mostrarlos
            if not respuesta or (isinstance(respuesta, dict) and "error" in respuesta):
                error_msg = respuesta.get("error", "Error desconocido") if isinstance(respuesta, dict) else "Error desconocido"
                messagebox.showerror("Error del servidor", error_msg)
                return
            
            messagebox.showinfo("Éxito", "Préstamo actualizado correctamente")
            self.cargar_datos_backend()
            self.limpiar_formulario()
            self.fila_seleccionada = None
        except Exception as e:
            print(f"[ERROR] Exception: {str(e)}")
            messagebox.showerror("Error", f"No se pudo actualizar el préstamo: {str(e)}")


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

        # ✅ El número se genera en el backend, no en el frontend
        # Solo limpiar el campo para crear nuevo préstamo
        self.numero_var.set("")

    def _leer_formulario(self):
        fecha_salida_raw = self.fecha_salida_var.get().strip()
        fecha_esperada_raw = self.fecha_esperada_var.get().strip()
        fecha_devolucion_raw = self.fecha_devolucion_var.get().strip()
        
        # Convertir fechas a ISO 8601
        fecha_salida = convertir_fecha_a_iso(fecha_salida_raw)
        fecha_esperada = convertir_fecha_a_iso(fecha_esperada_raw)
        fecha_devolucion = convertir_fecha_a_iso(fecha_devolucion_raw)
        
        # Si la conversión falló, mantener el valor original para que el validador lo detecte
        if fecha_salida_raw and fecha_salida is None:
            fecha_salida = fecha_salida_raw
        if fecha_esperada_raw and fecha_esperada is None:
            fecha_esperada = fecha_esperada_raw
        if fecha_devolucion_raw and fecha_devolucion is None:
            fecha_devolucion = fecha_devolucion_raw
        
        # NO enviar numero en CREATE (el servidor lo genera automáticamente)
        # Solo enviar si estamos editando (cuando numero no es el default "001")
        numero = self.numero_var.get().strip()
        
        datos = {
            "herramienta_codigo": self.herr_codigo_var.get().strip(),
            "responsable": self.responsable_var.get().strip(),
            "fecha_salida": fecha_salida,
            "fecha_esperada": fecha_esperada,
        }
        
        # Incluir numero solo en UPDATE (cuando no es el default)
        if numero and numero != "001":
            datos["numero"] = numero
        
        # Solo agregar fecha_devolucion si no está vacía
        if fecha_devolucion:
            datos["fecha_devolucion"] = fecha_devolucion
        
        return datos

    def actualizar_tabla(self):
        self.tabla.limpiar()
        for p in self.lista_prestamos:
            # ✅ Asegurar que fechas siempre sean YYYY-MM-DD (nunca ISO-8601)
            fecha_salida = p["fecha_salida"] if not ('T' in str(p["fecha_salida"])) else convertir_fecha_desde_iso(p["fecha_salida"])
            fecha_esperada = p["fecha_esperada"] if not ('T' in str(p["fecha_esperada"])) else convertir_fecha_desde_iso(p["fecha_esperada"])
            fecha_devolucion = p["fecha_devolucion"] if not ('T' in str(p["fecha_devolucion"])) else convertir_fecha_desde_iso(p["fecha_devolucion"])
            
            self.tabla.agregar_fila((
                p["numero"],
                p["herramienta_codigo"],
                p["responsable"],
                fecha_salida,
                fecha_esperada,
                fecha_devolucion,
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
            datos = self.lista_prestamos[index]

            self.numero_var.set(datos["numero"])
            self.herr_codigo_var.set(datos["herramienta_codigo"])
            self.responsable_var.set(datos["responsable"])
            
            # ✅ Asegurar que fechas siempre sean YYYY-MM-DD (nunca ISO-8601)
            fecha_salida = datos["fecha_salida"] if not ('T' in str(datos["fecha_salida"])) else convertir_fecha_desde_iso(datos["fecha_salida"])
            fecha_esperada = datos["fecha_esperada"] if not ('T' in str(datos["fecha_esperada"])) else convertir_fecha_desde_iso(datos["fecha_esperada"])
            fecha_devolucion = datos.get("fecha_devolucion", "")
            if fecha_devolucion and ('T' in str(fecha_devolucion)):
                fecha_devolucion = convertir_fecha_desde_iso(fecha_devolucion)
            
            self.fecha_salida_var.set(fecha_salida)
            self.fecha_esperada_var.set(fecha_esperada)
            self.fecha_devolucion_var.set(fecha_devolucion if fecha_devolucion else "")
        except Exception as e:
            print(f"[ERROR] seleccionar_fila: {e}")
            self.fila_seleccionada = None

    def obtener_filas(self):
        return self.lista_prestamos
