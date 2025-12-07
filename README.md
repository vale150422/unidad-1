# Proyecto Final - Instrucciones de instalación y ejecución

Este repositorio contiene un backend (Django) y un frontend en Python. A continuación se explican paso a paso las acciones necesarias en Windows (PowerShell) para que la aplicación funcione en tu equipo.

**Requisitos**

- Python 3.10+ instalado y en `PATH`.
- Git (opcional, para clonar/actualizar el repositorio).
- Conexión de red local si quieres probar con múltiples dispositivos.

**Estructura relevante**

- `backend/` : proyecto Django y base de datos SQLite.
- `backend/manage.py` : comandos de Django.
- `backend/initial_data.json` : datos de ejemplo.
- `frontend/` : cliente de escritorio/GUI en Python (ejecutable con `python -m frontend`).

-------------------------
Paso 1 — Preparar entornos virtuales (recomendado)

Recomiendo crear 2 entornos virtuales separados (uno para backend y otro para frontend). Abre PowerShell y ejecuta:

```powershell
# Desde la carpeta raíz del proyecto
cd "c:\Users\iA Tech\Downloads\proyecto final Valeria"

# Backend venv
python -m venv .venv-backend
.\.venv-backend\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r backend\requirements.txt

# Desactivar cuando termines con backend (opcional)
deactivate

# Frontend venv
python -m venv .venv-frontend
.\.venv-frontend\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r frontend\requirements.txt

# Desactivar
deactivate
```

Si PowerShell bloquea la activación por política de ejecución, ejecuta (con privilegios apropiados):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

-------------------------
Paso 2 — Configurar y arrancar el backend (Django)

1. Activa el entorno del backend y entra a la carpeta `backend`:

```powershell
cd "c:\Users\iA Tech\Downloads\proyecto final Valeria\backend"
.\..\.venv-backend\Scripts\Activate.ps1
```

2. Ejecuta migraciones y carga datos iniciales (si quieres usar los datos de ejemplo):

```powershell
python manage.py migrate
python manage.py loaddata initial_data.json
```

Nota: `loaddata` puede crear entradas duplicadas si ya hay datos. Si quieres empezar desde cero elimina `db.sqlite3` antes de `migrate`.

3. (Opcional) Crea un usuario administrador para acceder al admin de Django:

```powershell
python manage.py createsuperuser
```

4. Levanta el servidor de desarrollo:

```powershell
python manage.py runserver 0.0.0.0:8000
```

El backend quedará disponible en `http://127.0.0.1:8000/`.

-------------------------
Paso 3 — Ejecutar el frontend

1. Abre otra ventana de PowerShell y activa el entorno del frontend:

```powershell
cd "c:\Users\iA Tech\Downloads\proyecto final Valeria"
.\.venv-frontend\Scripts\Activate.ps1
```

2. Ejecuta el cliente:

```powershell
python -m frontend
```

3. Asegúrate de que el backend está corriendo en `http://127.0.0.1:8000/` antes de usar el frontend, porque el cliente se comunica con la API del backend.

-------------------------
Paso 4 — Comandos útiles

- Ejecutar tests Django:

```powershell
cd backend
.\..\.venv-backend\Scripts\Activate.ps1
python manage.py test
```

- Reiniciar migraciones (borrar la base de datos y rehacer todo):

```powershell
del db.sqlite3
python manage.py migrate
python manage.py loaddata initial_data.json
```

-------------------------
Solución de problemas comunes

- Error al activar venv: revisa la política de ejecución de PowerShell (`Set-ExecutionPolicy`).
- Error al instalar paquetes: asegúrate de usar la versión correcta de Python y que `pip` está actualizada.
- Puerto ocupado (8000): cambia el puerto en `runserver`, p.ej. `python manage.py runserver 0.0.0.0:8080`.
- `loaddata` falla por JSON inválido: verifica `backend\initial_data.json`.

-------------------------
Notas finales

- Si prefieres usar un solo entorno virtual, instala ambos `requirements.txt` en el mismo entorno, pero separar entornos evita conflictos.
- Para despliegue en producción no uses `runserver`; configura un servidor WSGI/ASGI (Gunicorn, Daphne, etc.) y una base de datos más robusta.
