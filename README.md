# Event Management

Plataforma para gestión de eventos, sesiones, usuarios y registros.

Arquitectura: API REST en Python (FastAPI) + SPA en Vue 3, contenerizados con Docker.

---

## Estructura del repositorio

```
event_management/
├── backend/    # API REST — FastAPI + SQLAlchemy + PostgreSQL
├── frontend/   # SPA — Vue 3 + Vite + Nginx
├── docker-compose.yml
└── .env.example
```

---

## Inicio rápido

### 1. Variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=tu_password_seguro
POSTGRES_DB=event_management
DATABASE_URL=postgresql+asyncpg://admin:tu_password_seguro@db:5432/event_management
JWT_SECRET=una_cadena_aleatoria_larga
PYTHONPATH=/app
ADMIN_NAME=Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=tu_password_admin
```

### 2. Levantar con Docker

```bash
docker compose up --build
```

Al iniciar, el backend ejecuta las migraciones y crea el usuario administrador inicial con las credenciales del `.env`.

| Servicio | URL |
|---|---|
| Frontend | http://localhost:80 |
| API (Swagger) | http://localhost:8000/docs |
| API (ReDoc) | http://localhost:8000/redoc |

---

## Backend

API REST construida con **FastAPI** siguiendo arquitectura hexagonal (Ports & Adapters).

### Stack

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje |
| FastAPI | Framework web |
| SQLAlchemy 2 + asyncpg | ORM async |
| SQLModel | Modelos ORM |
| Alembic | Migraciones |
| PostgreSQL 16 | Base de datos |
| PyJWT + bcrypt | Auth y cifrado |
| Poetry | Dependencias |
| pytest | Tests unitarios |

### Arquitectura

```
Dominio  ←  Aplicación  ←  Infraestructura
```

- **Dominio**: entidades, value objects, puertos e interfaces. Sin dependencias externas.
- **Aplicación**: casos de uso y DTOs. Orquesta el dominio.
- **Infraestructura**: repositorios SQLAlchemy, routers FastAPI, seguridad JWT.

### Roles

| Rol | Permisos |
|---|---|
| `attendee` | Ver eventos y sesiones, registrarse a eventos |
| `organizer` | Todo lo anterior + crear/editar/eliminar eventos y sesiones |
| `admin` | Todo lo anterior + gestionar usuarios y asignar roles |

### Endpoints principales

**Usuarios** `/api/v1/users`

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| POST | `/` | Registrar usuario | Público |
| POST | `/login` | Login → JWT | Público |
| GET | `/{user_id}` | Obtener usuario | Autenticado |
| GET | `/search/{email}` | Buscar por email | Autenticado |
| PATCH | `/{user_id}/role` | Cambiar rol | Admin |
| DELETE | `/{user_id}` | Eliminar usuario | Admin |

**Eventos** `/api/v1/events`

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| GET | `/` | Listar todos | Autenticado |
| GET | `/search/{name}` | Buscar por nombre | Autenticado |
| GET | `/{event_id}` | Obtener evento | Autenticado |
| POST | `/` | Crear evento | Admin / Organizer |
| PUT | `/{event_id}` | Actualizar | Admin / Organizer |
| DELETE | `/{event_id}` | Eliminar | Admin / Organizer |

**Sesiones** `/api/v1/events/{event_id}/sessions`

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| GET | `/` | Listar sesiones | Autenticado |
| GET | `/{session_id}` | Obtener sesión | Autenticado |
| POST | `/` | Crear sesión | Admin / Organizer |
| PUT | `/{session_id}` | Actualizar | Admin / Organizer |
| DELETE | `/{session_id}` | Eliminar | Admin / Organizer |

**Registros** `/api/v1/register`

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| POST | `/` | Registrarse a un evento | Autenticado |
| GET | `/` | Ver mis registros | Autenticado |

### Tests

```bash
cd backend
pytest tests/ -v
```

Los tests cubren la capa de dominio (entidades, value objects, reglas de negocio). No requieren base de datos ni servidor activo.

### Desarrollo local (sin Docker)

```bash
cd backend
uvicorn src.main:app --reload
```

Requiere PostgreSQL local. Ajusta el host en `DATABASE_URL` de `db` a `localhost` en tu `.env`.

---

## Frontend

SPA construida con **Vue 3 + Vite**, servida en producción por Nginx.

### Vistas

| Ruta | Descripción | Acceso |
|---|---|---|
| `/login` | Login y registro de cuenta | Público |
| `/events` | Lista de eventos, búsqueda, CRUD | Autenticado |
| `/events/:id` | Detalle + sesiones del evento | Autenticado |
| `/registrations` | Mis registros | Autenticado |
| `/users` | Gestión de usuarios | Solo admin |

### Desarrollo local (sin Docker)

Requiere el backend corriendo en `http://localhost:8000`.

```bash
cd frontend
npm install
npm run dev
```

Accede en `http://localhost:5173`. El proxy de Vite redirige `/api` al backend.

---

## Desarrollo local completo (sin Docker)

Terminal 1 — base de datos (o usar Docker solo para Postgres):
```bash
docker compose up db
```

Terminal 2 — backend:
```bash
cd backend
uvicorn src.main:app --reload
```

Terminal 3 — frontend:
```bash
cd frontend
npm install
npm run dev
```
