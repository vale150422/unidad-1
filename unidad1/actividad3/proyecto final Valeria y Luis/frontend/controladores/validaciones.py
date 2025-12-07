import re
from datetime import datetime

class Validaciones:

    # ===========================
    # VALIDACIONES GENERALES
    # ===========================

    def campo_vacio(self, valor):
        return valor is None or str(valor).strip() == ""

    def validar_fecha(self, fecha):
        """
        Acepta formatos:
        - YYYY-MM-DD (lo más importante)
        - YYYY/MM/DD
        - YYYY-MM-DDTHH:MM:SSZ (ISO 8601 ya convertido)
        """
        if self.campo_vacio(fecha):
            return False

        fecha_str = str(fecha).strip()
        
        # Si ya está convertida a ISO 8601
        if "T" in fecha_str and "Z" in fecha_str:
            return True

        # Formatos aceptados para entrada
        formatos = ["%Y-%m-%d", "%Y/%m/%d"]

        for f in formatos:
            try:
                datetime.strptime(fecha_str, f)
                return True
            except:
                pass

        return False

    def validar_texto(self, valor):
        """Solo letras y espacios"""
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚÑáéíóúñ ]+$", valor))

    def validar_codigo(self, valor):
        """Letras, números, guiones y guion bajo"""
        return bool(re.match(r"^[A-Za-z0-9_\-]+$", valor))


    # ===========================
    # VALIDACIONES HERRAMIENTAS
    # ===========================

    def validar_herramienta(self, data):
        errores = []

        # Código (generado automáticamente, no validar si está vacío)
        codigo = data.get("codigo", "").strip()
        if codigo and not self.validar_codigo(codigo):
            errores.append("El código solo puede contener letras, números y guiones.")

        # Nombre
        if self.campo_vacio(data.get("nombre")):
            errores.append("El nombre no puede estar vacío.")
        elif not self.validar_texto(data.get("nombre")):
            errores.append("El nombre solo puede contener letras.")

        # Categoría
        if self.campo_vacio(data.get("categoria")):
            errores.append("La categoría es obligatoria.")

        # Ubicación
        if self.campo_vacio(data.get("ubicacion")):
            errores.append("La ubicación es obligatoria.")

        # Estado
        estado_valido = data.get("estado", "").lower() in ["disponible", "prestada", "dañada"]
        if data.get("estado") and not estado_valido:
            errores.append("El estado debe ser: disponible, prestada o dañada.")

        return errores


    # ===========================
    # VALIDACIONES PRÉSTAMOS
    # ===========================

    def validar_prestamo(self, data):
        errores = []

        # Número (se genera automáticamente, validar solo si viene)
        numero = data.get("numero", "").strip()
        if numero and not numero.isdigit():
            # Si no es un dígito puro, puede ser que sea un formato como "PR-001"
            # En ese caso, ignorar validación ya que lo genera el servidor
            pass

        # Código herramienta
        if self.campo_vacio(data.get("herramienta_codigo")):
            errores.append("Debe especificar la herramienta.")

        # Responsable
        if self.campo_vacio(data.get("responsable")):
            errores.append("El responsable es obligatorio.")
        elif not self.validar_texto(data.get("responsable")):
            errores.append("El responsable solo puede contener letras y espacios.")

        # Fechas obligatorias (salida y esperada)
        for campo in ["fecha_salida", "fecha_esperada"]:
            if self.campo_vacio(data.get(campo)):
                errores.append(f"La {campo.replace('_', ' ')} es obligatoria.")
            elif not self.validar_fecha(data.get(campo)):
                errores.append(f"La {campo.replace('_', ' ')} debe tener formato YYYY-MM-DD.")

        # Fecha de devolución (opcional)
        if data.get("fecha_devolucion"):
            if not self.validar_fecha(data.get("fecha_devolucion")):
                errores.append("La fecha de devolución debe tener formato YYYY-MM-DD.")

        # ✅ NUEVA VALIDACIÓN: fecha_esperada >= fecha_salida
        fecha_salida = data.get("fecha_salida", "").strip()
        fecha_esperada = data.get("fecha_esperada", "").strip()
        
        if fecha_salida and fecha_esperada and self.validar_fecha(fecha_salida) and self.validar_fecha(fecha_esperada):
            try:
                # Extraer fecha de formatos ISO 8601 o YYYY-MM-DD
                fs = datetime.strptime(fecha_salida[:10], "%Y-%m-%d")
                fe = datetime.strptime(fecha_esperada[:10], "%Y-%m-%d")
                
                if fe < fs:
                    errores.append("La fecha esperada no puede ser anterior a la fecha de salida.")
            except:
                pass  # Si hay error en parsing, ya lo capturó la validación anterior

        # ✅ NUEVA VALIDACIÓN: fecha_devolucion >= fecha_salida
        fecha_devolucion = data.get("fecha_devolucion", "").strip()
        if fecha_devolucion and fecha_salida and self.validar_fecha(fecha_devolucion) and self.validar_fecha(fecha_salida):
            try:
                fd = datetime.strptime(fecha_devolucion[:10], "%Y-%m-%d")
                fs = datetime.strptime(fecha_salida[:10], "%Y-%m-%d")
                
                if fd < fs:
                    errores.append("La fecha de devolución no puede ser anterior a la fecha de salida.")
            except:
                pass

        return errores