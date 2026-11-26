# Sistema de Gestión de Trámites de Grado

Aplicación web para gestionar el trámite de grado de los estudiantes: registro del trámite, entrega de documentos, pago, paz y salvo, asignación a ceremonias y reportes. Tiene tres roles (estudiante, coordinación y administrador) con permisos distintos.

> Proyecto académico de Ingeniería de Software. Equipo: **[Jhonatan Vanegas]**, 

## Qué hace

- **Estudiante:** crea su cuenta, registra su trámite de grado, entrega los documentos requeridos y consulta el estado de su pago, paz y salvo y ceremonia.
- **Coordinación:** ve todos los trámites, confirma pagos, aprueba paz y salvo, valida documentos, crea ceremonias, asigna estudiantes y genera reportes en PDF.
- **Administrador:** todo lo anterior, más la gestión de usuarios y roles, facultades, programas y catálogos.
- **Notificaciones por correo** cuando cambia el estado de un pago o paz y salvo, o se crea un usuario.
- **Reportes en PDF** filtrables por estado, fechas y programa.

## Tecnologías

| Capa | Tecnologías |
|---|---|
| Frontend | Svelte 5, Vite, DataTables |
| Backend | Python, FastAPI, Pydantic |
| Base de datos | PostgreSQL (Neon) |
| Seguridad | JWT (python-jose), contraseñas con bcrypt, permisos por rol |
| Otros | ReportLab (PDF), SMTP (correos), Netlify (frontend) |

## Arquitectura

```
Frontend (Svelte)  ──HTTP/JSON + JWT──▶  API FastAPI  ──psycopg2──▶  PostgreSQL
                                           │
                                           └── EmailService (SMTP)
```

La API está organizada en capas: `routes` (entrada), `controllers` (lógica y acceso a datos), `models` (validación) y `services` (correo).

La base de datos tiene 12 tablas (ver `app/sql/script.sql`).

## Estructura del proyecto

```
app/
  main.py            # aplicación FastAPI
  auth.py            # JWT y contraseñas
  auth_middleware.py # control de acceso por rol
  config/            # conexión a la base de datos
  controllers/       # lógica de cada módulo
  models/            # modelos Pydantic
  routes/            # endpoints
  services/          # envío de correos
  sql/script.sql     # esquema de la base de datos
frontend/
  src/lib/           # componentes Svelte (paneles, tablas, formularios)
```

## Cómo ejecutarlo

### Requisitos

- Python 3.11 o superior
- Node.js 20.19 o superior
- Una base PostgreSQL (por ejemplo, un proyecto gratuito en [Neon](https://neon.tech))

### 1. Base de datos

Ejecuta el script `app/sql/script.sql` en tu base de datos para crear las tablas.

### 2. Variables de entorno

Copia `.env.example` a `.env` en la carpeta raíz y completa tus datos:

```
DB_HOST=tu-host.neon.tech
DB_PORT=5432
DB_USER=usuario
DB_PASSWORD=tu_clave
DB_NAME=nombre_bd
SMTP_USER=correo@gmail.com
SMTP_PASS=clave_de_aplicacion
```

Si no configuras `SMTP_USER` y `SMTP_PASS`, el sistema funciona igual pero no envía correos.

### 3. Backend

```bash
python -m venv .venv
.venv\Scripts\activate          # en Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

La API queda en http://127.0.0.1:8000 y su documentación interactiva en http://127.0.0.1:8000/docs.

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173/index.html (usa `localhost`, no `127.0.0.1`).

## Estado del proyecto y mejoras pendientes

El flujo principal funciona de extremo a extremo. Estas son las mejoras previstas:

- Validar en el servidor las transiciones de estado (por ejemplo, no completar un trámite con el pago pendiente).
- Forzar el rol «estudiante» al crear una cuenta desde el registro público.
- Guardar un historial de cambios de cada trámite.
- Agregar pruebas automáticas y desplegar el backend para tener una demo en línea.

## Autores

- **[Jhonatan Vanegas]** · [GitHub](https://github.com/vanegasjhoy)


