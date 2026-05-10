# Event Management — Frontend

SPA construida con Vue 3 + Vite que consume la API REST del backend.

## Stack

| Tecnología | Uso |
|---|---|
| Vue 3 (Composition API) | Framework |
| Vue Router 4 | Navegación SPA |
| Axios | Llamadas HTTP |
| Vite | Bundler / dev server |
| Nginx | Servidor en producción |

## Vistas

| Ruta | Vista | Acceso |
|---|---|---|
| `/login` | Login / Registro de cuenta | Público |
| `/events` | Lista de eventos, búsqueda, CRUD | Autenticado |
| `/events/:id` | Detalle de evento y sus sesiones | Autenticado |
| `/registrations` | Mis registros a eventos | Autenticado |
| `/users` | Gestión de usuarios (buscar, cambiar rol, eliminar) | Solo admin |

## Correr en desarrollo local

Requiere tener el backend corriendo en `http://localhost:8000`.

```bash
npm install
npm run dev
```

Accede en `http://localhost:5173`. El proxy de Vite redirige `/api` al backend automáticamente.

## Correr con Docker

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Nginx sirve el build en `http://localhost:80` y proxea `/api` hacia el servicio `api`.

## Estructura

```
frontend/
├── src/
│   ├── main.js
│   ├── App.vue           # Layout principal + navbar
│   ├── router/index.js   # Rutas y guards de autenticación
│   ├── services/api.js   # Cliente Axios con interceptores JWT
│   └── views/
│       ├── LoginView.vue
│       ├── EventsView.vue
│       ├── EventDetailView.vue
│       ├── RegistrationsView.vue
│       └── UsersView.vue
├── nginx.conf
├── Dockerfile
└── package.json
```
