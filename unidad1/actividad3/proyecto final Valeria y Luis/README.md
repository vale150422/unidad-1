**Proyecto de Gestión de Herramientas**

## Descripción General

IHEP es una aplicación de escritorio diseñada para la gestión integral de inventario de herramientas y control de préstamos en entornos empresariales. Implementa una arquitectura multicapa con un backend REST basado en Django y una interfaz gráfica de usuario desarrollada en Tkinter, proporcionando una solución robusta y escalable para la administración de recursos.

Este repositorio contiene una aplicación con backend en Django (API REST) y un frontend en Python. El backend expone endpoints para gestionar herramientas y préstamos; el frontend es una interfaz de cliente que consume la API.

**Requisitos**
- **Python**: 3.11 o superior
- **Entorno**: se recomienda usar un entorno virtual (`venv`) para instalar dependencias

**Instalación (Windows / PowerShell)**
- **Clonar / abrir el repositorio**: abre una terminal en la carpeta raíz del proyecto (donde está `manage.py`).
- **Crear y activar entorno virtual**:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
```

- **Instalar dependencias** (instala tanto las dependencias del backend como del frontend en el mismo entorno):

```powershell
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

**Configurar base de datos y datos iniciales**
- La aplicación usa SQLite por defecto y el fichero de base de datos se crea en `backend/db.sqlite3`.
- Ejecuta migraciones y carga los datos de ejemplo incluidos en `backend/initial_data.json`:

```powershell
# Desde la raíz del proyecto
python backend/manage.py migrate
python backend/manage.py loaddata backend/initial_data.json
```

**Ejecutar el backend (API)**
- Inicia el servidor de desarrollo Django:

```powershell
python backend/manage.py runserver 0.0.0.0:8000
```

- La API queda disponible en `http://127.0.0.1:8000/api/`.
- Endpoints principales:
	- **Herramientas**: `GET/POST/PUT/DELETE` en `http://127.0.0.1:8000/api/herramientas/`
	- **Préstamos**: `GET/POST/PUT/DELETE` en `http://127.0.0.1:8000/api/prestamos/`
	- **Búsqueda**: `GET` en `http://127.0.0.1:8000/api/buscar/`

**Ejecutar el frontend (cliente)**
- El frontend se puede ejecutar como un script de Python. Desde la raíz del proyecto:

```powershell
# Opción 1 (recomendada)
python -m frontend

# Opción 2
python frontend\__main__.py
```

La interfaz cliente se conecta a la API en `http://127.0.0.1:8000/api/` por defecto; asegúrate de tener el backend en ejecución antes de abrir el frontend.

**Crear superusuario (panel admin)**
- Si necesitas acceder al panel de administración de Django:

```powershell
python backend/manage.py createsuperuser
# luego acceder a http://127.0.0.1:8000/admin/
```

**Ejecutar pruebas**
- Si deseas ejecutar las pruebas definidas (si las hay):

```powershell
python backend/manage.py test
```

**Archivos y rutas importantes**
- **Backend**: `backend/` (contiene el proyecto Django y la base de datos `backend/db.sqlite3`)
- **Frontend**: `frontend/` (cliente Python)
- **Dependencias backend**: `backend/requirements.txt`
- **Dependencias frontend**: `frontend/requirements.txt`
- **Fixture de datos**: `backend/initial_data.json`

**Notas y recomendaciones**
- Este proyecto se entrega en modo desarrollo (`DEBUG=True`). No desplegar con estas configuraciones en producción sin revisarlas.
- Para ambientes de producción, considere cambiar la base de datos a PostgreSQL/MySQL, configurar `ALLOWED_HOSTS`, `SECRET_KEY` y servir archivos estáticos adecuadamente.



