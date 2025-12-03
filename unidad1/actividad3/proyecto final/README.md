# IHEP - Sistema de Gestión de Inventario de Herramientas y Préstamos
Descripción General

IHEP es una aplicación de escritorio profesional para la gestión integral de herramientas y el control de préstamos en empresas.
Utiliza un backend REST en Django y un frontend con Tkinter bajo una arquitectura MVC, permitiendo una administración eficiente, modular y escalable.

Su diseño facilita el registro, préstamo, devolución, monitoreo y respaldo automático de toda la información de inventario.

 Características Principales

 Gestión de Herramientas
Registro con código único, estado, categoría, ubicación y disponibilidad.

 Control de Préstamos
Manejo completo del ciclo de préstamo: salida, devolución esperada y real.

 Búsqueda en Tiempo Real
Filtros avanzados integrados en Tkinter.

 Respaldos Automáticos
Se generan JSON periódicos sin bloquear la aplicación (hilos daemon).

 Interfaz Gráfica Tkinter (MVC)
Frontend modular, intuitivo y totalmente separado del backend.

 API REST Django
Endpoints completos y documentados para integraciones externas.

 Validaciones Robustas
Validación estricta tanto en el frontend como en la API.

 Requisitos Técnicos
 Requisitos del Sistema

Python ≥ 3.12

SQLite 3 (incluido con Python)

Memoria mínima: 512 MB

100 MB de espacio libre

 Dependencias
Django==5.2.8
djangorestframework==3.16.1
django-cors-headers==4.9.0
requests==2.32.5

 Instalación
1. Clonar el Repositorio
git clone https://github.com/Sebastian-Poloche/POE_/tree/main/trabajo_final

2. Crear Entorno Virtual
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

3. Instalar Dependencias
pip install -r requirements.txt

4. Migrar Base de Datos
cd backend
python manage.py migrate

 Ejecución del Sistema
 Ejecución Recomendada
python iniciar_ihep.py


Esto inicia automáticamente:

Backend Django → http://127.0.0.1:8000

API REST → http://127.0.0.1:8000/api

Frontend Tkinter

Hilo de respaldos automáticos

 Ejecución Manual
 Terminal 1 — Backend
cd backend
python manage.py runserver 127.0.0.1:8000

 Terminal 2 — Frontend
python main.py

 Arquitectura General

IHEP utiliza una arquitectura 3 capas + MVC para el frontend:

1. Capa de Presentación (Frontend Tkinter)

Vistas en frontend/views/

Controladores en frontend/controllers/

Modelos REST en frontend/models/

Lógica MVC completa

2. Capa de Negocio (Backend Django REST)

Serializers

ViewSets

Validaciones

Ruteo de API

3. Capa de Persistencia

Modelos Django ORM

SQLite

Migraciones versionadas

 Validaciones
 Herramientas

Código → exactamente 7 caracteres alfanuméricos

Nombre → requerido

Ubicación → requerido

Categoría → “Enviar” o “Devolver”

Estado → estado válido del inventario

Código único en la BD

 Préstamos

Número → 7 caracteres alfanuméricos

Responsable → requerido

Herramienta → debe existir y estar disponible

Fechas → salida < esperada < devolución

Estado coherente según el flujo

 Configuración
 Variables de Entorno
BACKEND_URL=http://127.0.0.1:8000/api
BACKEND_PORT=8000
BACKEND_HOST=127.0.0.1
INTERVALO_BACKUP_SEG=300

 Archivo config.py

Controla:

URLs del backend

Frecuencia de respaldos

Parametrización de rutas

 Sistema de Respaldos
 Funcionamiento

Respaldos automáticos cada 300s (configurable)

Se ejecutan en un hilo daemon

No bloquean la interfaz

Guardados en JSON

 Ubicación
frontend/backups/

 Desarrollo y Mantenimiento
 Pruebas
cd backend
python manage.py test

 Migraciones
python manage.py makemigrations
python manage.py migrate

 Django Admin
http://127.0.0.1:8000/admin/

 Rendimiento

Hasta 10,000 registros sin pérdida significativa de rendimiento

Consultas REST < 100 ms

Respaldos < 1 segundo

 Seguridad
Actualmente

Validación robusta en API

CORS para entorno local

SECRET_KEY predeterminada (solo desarrollo)

Para Producción

Cambiar SECRET_KEY

Desactivar DEBUG

Usar HTTPS

Autenticación por token

Configurar ALLOWED_HOSTS

Servidor WSGI (Gunicorn)

 Cumplimiento de Requerimientos

IHEP cumple con:

Gestión total de herramientas

Gestión completa de préstamos

Validaciones estrictas

Interfaz gráfica funcional con MVC

Sistema de respaldo

API REST funcional

 Autores

Proyecto desarrollado para POE - 2025
Creado por:

## Autores
- Katherin Valeria Vásquez Murillo
- Carlos Andres Morales Rojas
- Luis Alejandro Erazo Rios  
- GitHub: https://github.com/vale150422

Gap404

 Versión
 Versión 1.0 – 30 Nov 2025

Lanzamiento inicial

CRUD completo



