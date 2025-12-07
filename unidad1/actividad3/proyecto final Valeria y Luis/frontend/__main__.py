"""
Punto de entrada del Sistema IHEP
Inicia la interfaz gráfica Tkinter
"""

from vistas.interfaz_principal import InterfazPrincipal

if __name__ == "__main__":
    app = InterfazPrincipal()
    app.mainloop()
