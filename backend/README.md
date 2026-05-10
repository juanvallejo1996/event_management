# Event Management API

REST API para la gestión de eventos, sesiones, usuarios y registros, construida con FastAPI siguiendo arquitectura hexagonal (Ports & Adapters).

## Stack tecnológico

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje |
| FastAPI | Framework web |
| SQLAlchemy 2 + asyncpg | ORM async + driver PostgreSQL |
| SQLModel | Modelos ORM |
| Alembic | Migraciones de base de datos |
| PostgreSQL 16 | Base de datos |
| Poetry | Gestión de dependencias |
| PyJWT + bcrypt | Autenticación y cifrado |
| Docker + Docker Compose | Contenerización |
| pytest | Tests unitarios |

---

## Arquitectura

El proyecto sigue **arquitectura hexagonal (Ports & Adapters)**, organizada en tres capas:

```
Dominio  ←  Aplicación  ←  Infraestructura
```

- **Dominio**: entidades puras, value objects, puertos (interfaces) y excepciones de negocio. Sin dependencias externas.
- **Aplicación**: casos de uso y DTOs. Orquesta el dominio sin conocer la infraestructura.
- **Infraestructura**: repositorios SQLAlchemy, routers FastAPI, modelos ORM, seguridad JWT.

---

## Requisitos

- Docker y Docker Compose
- (Opcional, para desarrollo local) Python 3.12 + pyenv + Poetry

---

## Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd event_management
```

### 2. Crear el archivo de variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```env
# PostgreSQL
POSTGRES_USER=admin
POSTGRES_PASSWORD=tu_contraseña_segura
POSTGRES_DB=event_management

# Application
# Para Docker usa 'db' como host; para desarrollo local usa 'localhost'
DATABASE_URL=postgresql+asyncpg://admin:tu_contraseña_segura@db:5432/event_management

JWT_SECRET=una_cadena_aleatoria_y_segura

PYTHONPATH=/app

# Usuario administrador inicial (se crea al arrancar si no existe)
ADMIN_NAME=Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=tu_password_admin_seguro
```

> **Nota:** En `DATABASE_URL`, el host debe ser `db` (nombre del servicio en Docker Compose). Para desarrollo local, cámbialo a `localhost`.

---

## Ejecución con Docker (recomendado)

```bash
# Construir e iniciar todos los servicios
docker compose up --build

# En segundo plano
docker compose up --build -d
```

Al iniciar, el contenedor de la API:
1. Espera a que PostgreSQL esté listo
2. Ejecuta las migraciones automáticamente (`alembic upgrade head`)
3. Crea el usuario administrador inicial si no existe
4. Inicia el servidor en `http://localhost:8000`


## Documentación de la API

Con el proyecto en ejecución, accede a la documentación interactiva:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Roles de usuario

| Rol | Descripción |
|---|---|
| `attendee` | Usuario estándar. Puede registrarse a eventos y consultar información. |
| `organizer` | Puede crear, editar y eliminar eventos y sesiones. |
| `admin` | Acceso total. Además puede gestionar usuarios y asignar roles. |

El primer usuario administrador se crea automáticamente al arrancar la aplicación con las credenciales definidas en `.env`.

### Endpoints

#### Usuarios — `/api/v1/users`

| Método | Ruta | Descripción | Rol requerido |
|---|---|---|---|
| POST | `/` | Registrar usuario | Público |
| POST | `/login` | Login → retorna JWT | Público |
| GET | `/{user_id}` | Obtener usuario por ID | Autenticado |
| GET | `/search/{email}` | Buscar usuario por email | Autenticado |
| PATCH | `/{user_id}/role` | Cambiar rol de un usuario | Admin |
| DELETE | `/{user_id}` | Eliminar usuario | Admin |

#### Eventos — `/api/v1/events`

| Método | Ruta | Descripción | Rol requerido |
|---|---|---|---|
| GET | `/{event_id}` | Obtener evento | Autenticado |
| GET | `/search/{name}` | Buscar eventos por nombre | Autenticado |
| POST | `/` | Crear evento | Admin / Organizer |
| PUT | `/{event_id}` | Actualizar evento | Admin / Organizer |
| DELETE | `/{event_id}` | Eliminar evento | Admin / Organizer |

> Los eventos solo pueden crearse con fechas futuras y con fecha de fin posterior a la de inicio.

#### Sesiones — `/api/v1/events/{event_id}/sessions`

| Método | Ruta | Descripción | Rol requerido |
|---|---|---|---|
| GET | `/` | Listar sesiones del evento | Autenticado |
| GET | `/{session_id}` | Obtener sesión | Autenticado |
| POST | `/` | Crear sesión en un evento | Admin / Organizer |
| PUT | `/{session_id}` | Actualizar sesión | Admin / Organizer |
| DELETE | `/{session_id}` | Eliminar sesión | Admin / Organizer |

> Las sesiones deben estar dentro del rango de fechas del evento al que pertenecen.

#### Registros — `/api/v1/register`

| Método | Ruta | Descripción | Rol requerido |
|---|---|---|---|
| POST | `/` | Registrarse a un evento | Autenticado |
| GET | `/` | Ver mis registros | Autenticado |

### Autenticación

Los endpoints protegidos requieren un header:

```
Authorization: Bearer <token>
```

El token se obtiene en `POST /api/v1/users/login`.

---

## Desarrollo local (sin Docker)

### 1. Configurar Python con pyenv

```bash
pyenv install 3.12.4
pyenv virtualenv 3.12.4 venv_events_management
pyenv activate venv_events_management
```

### 2. Instalar dependencias con Poetry

```bash
poetry install
```

### 3. Configurar variables de entorno

Edita `.env` y cambia el host en `DATABASE_URL` de `db` a `localhost`:

```env
DATABASE_URL=postgresql+asyncpg://admin:tu_contraseña@localhost:5432/event_management
```

### 4. Crear la base de datos en PostgreSQL local

```bash
createdb -U admin event_management
```

### 5. Ejecutar migraciones

```bash
alembic upgrade head
```

### 6. Iniciar el servidor

```bash
uvicorn src.main:app --reload
```

---

## Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con resumen de cobertura por archivo
pytest tests/ -v --tb=short
```

Los tests cubren la capa de **dominio**: entidades, value objects y reglas de negocio. No requieren base de datos ni servidor activo.

---

## Estructura del proyecto

```
event_management/
├── src/
│   ├── domain/                        # Capa de dominio (núcleo)
│   │   ├── events/
│   │   │   ├── event.py               # Entidad Event
│   │   │   ├── event_status.py        # Enum de estados
│   │   │   ├── event_exceptions.py    # Excepciones de negocio
│   │   │   ├── ports/
│   │   │   │   └── event_repository.py  # Puerto (interfaz)
│   │   │   └── value_objects/
│   │   │       └── event_capacity.py
│   │   ├── sessions/
│   │   ├── registrations/
│   │   └── users/
│   │
│   ├── application/                   # Capa de aplicación
│   │   ├── events/
│   │   │   ├── dto/                   # Data Transfer Objects
│   │   │   └── use_cases/             # Casos de uso
│   │   ├── sessions/
│   │   ├── registrations/
│   │   └── users/
│   │
│   ├── infrastructure/                # Capa de infraestructura
│   │   ├── database/
│   │   │   ├── session.py             # Engine y sesión async
│   │   │   └── seed.py                # Seeder del usuario admin inicial
│   │   ├── repositories/
│   │   │   ├── sqlalchemy/            # Repositorios PostgreSQL
│   │   │   └── in_memory/             # Repositorios en memoria (testing)
│   │   ├── security/
│   │   │   └── jwt_token_service.py   # Implementación JWT
│   │   └── http/
│   │       ├── routers/               # Routers FastAPI
│   │       ├── requests/              # Modelos de entrada (Pydantic)
│   │       ├── responses/             # Modelos de salida (Pydantic)
│   │       ├── auth_dependencies.py   # get_current_user, require_admin, require_admin_or_organizer
│   │       ├── *_dependencies.py      # Inyección de dependencias por dominio
│   │       └── exception_handlers.py  # Manejo global de errores
│   │
│   ├── config/
│   │   └── container.py               # Contenedor de servicios singleton
│   └── main.py                        # Entry point FastAPI
│
├── alembic/                           # Migraciones de base de datos
├── tests/
│   └── domain/                        # Tests unitarios de dominio (sin BD)
│       ├── events/
│       ├── sessions/
│       ├── registrations/
│       └── users/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── pyproject.toml
└── poetry.lock
```
