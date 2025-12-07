import tkinter as tk
from controladores.auth_controller import AuthController
from vistas.login_view import LoginView
from vistas.admin_dashboard import AdminDashboardView
from vistas.employee_dashboard import EmployeeDashboardView


class MainController:
    def __init__(self, root):
        self.root = root
        self.current_view = None

        # Controlador de autenticación (conexión a Django)
        self.auth_controller = AuthController()

    # -----------------------------
    # UTILIDAD: Cambiar de vista
    # -----------------------------
    def _show_view(self, view_class, **kwargs):
        # Destruir vista actual si existe
        if self.current_view is not None:
            self.current_view.destroy()

        # Crear nueva vista
        self.current_view = view_class(self.root, self, **kwargs)
        self.current_view.pack(fill="both", expand=True)

    # -----------------------------
    # MOSTRAR LOGIN
    # -----------------------------
    def show_login(self):
        self._show_view(LoginView)

    # -----------------------------
    # PROCESAR LOGIN
    # -----------------------------
    def login(self, username, password):
        user_data = self.auth_controller.authenticate(username, password)

        if user_data is None:
            return False  # Vista mostrará el error

        # Identificar rol
        role = user_data.get("role")

        if role == "admin":
            self.show_admin_dashboard(user_data)

        elif role == "empleado":
            self.show_employee_dashboard(user_data)

        else:
            print("⚠ Rol no reconocido")
            return False

        return True

    # -----------------------------
    # DASHBOARD ADMIN
    # -----------------------------
    def show_admin_dashboard(self, user):
        self._show_view(AdminDashboardView, user=user)

    # -----------------------------
    # DASHBOARD EMPLEADO
    # -----------------------------
    def show_employee_dashboard(self, user):
        self._show_view(EmployeeDashboardView, user=user)

    # -----------------------------
    # CERRAR SESIÓN
    # -----------------------------
    def logout(self):
        self.show_login()
