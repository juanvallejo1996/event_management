<template>
  <div id="root">
    <nav v-if="isLoggedIn">
      <span class="brand">Event Management</span>
      <router-link to="/events">Eventos</router-link>
      <router-link to="/registrations">Mis Registros</router-link>
      <router-link v-if="isAdmin" to="/users">Usuarios</router-link>
      <span class="spacer"></span>
      <div class="user-pill">
        <div class="user-avatar">{{ initials }}</div>
        <div class="user-meta">
          <span class="user-name">{{ user?.name }}</span>
          <span :class="`user-role role-${user?.role}`">{{ user?.role }}</span>
        </div>
      </div>
      <button class="btn-logout" @click="logout">&#x2192; Cerrar sesión</button>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

function readAuth() {
  const token = localStorage.getItem('token')
  const u = localStorage.getItem('user')
  return { token, user: u ? JSON.parse(u) : null }
}

const auth = ref(readAuth())

watch(() => route.path, () => { auth.value = readAuth() })

const isLoggedIn = computed(() => !!auth.value.token)
const user = computed(() => auth.value.user)
const isAdmin = computed(() => user.value?.role === 'admin')
const initials = computed(() => {
  const name = user.value?.name || ''
  return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase() || '?'
})

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #f0f2f5; color: #333; }

nav {
  background: #1a202c;
  padding: 0 1.5rem;
  height: 52px;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
}
.brand { font-weight: 700; font-size: 1rem; color: white; }
nav a { color: #a0aec0; text-decoration: none; font-size: 0.9rem; }
nav a:hover, nav a.router-link-active { color: white; }
.spacer { flex: 1; }

.user-pill {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #2d3748;
  border-radius: 999px;
  padding: 0.3rem 0.85rem 0.3rem 0.3rem;
}
.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #4299e1;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.user-meta { display: flex; flex-direction: column; line-height: 1.2; }
.user-name { font-size: 0.82rem; color: white; font-weight: 600; white-space: nowrap; }
.user-role {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.role-admin { color: #fc8181; }
.role-organizer { color: #68d391; }
.role-attendee { color: #76e4f7; }

.btn-logout {
  background: #e53e3e;
  border: none;
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  white-space: nowrap;
  transition: background 0.15s;
}
.btn-logout:hover { background: #c53030; }

main { padding: 1.75rem; max-width: 960px; margin: 0 auto; }

h2 { font-size: 1.4rem; color: #1a202c; margin-bottom: 1.25rem; }
h3 { font-size: 1rem; color: #2d3748; margin-bottom: 0.3rem; }

.card {
  background: white;
  border-radius: 8px;
  padding: 1.1rem 1.25rem;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}
.card-body { flex: 1; }
.card h3 { margin: 0 0 0.2rem; }
.card p { color: #718096; font-size: 0.875rem; margin: 0.15rem 0; }

.row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.search-row { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
.search-row input { flex: 1; }

form { display: flex; flex-direction: column; gap: 0.5rem; }
label { font-size: 0.82rem; font-weight: 600; color: #4a5568; }
input, select, textarea {
  padding: 0.45rem 0.65rem;
  border: 1px solid #cbd5e0;
  border-radius: 5px;
  font-size: 0.9rem;
  width: 100%;
  background: white;
}
input:focus, select:focus, textarea:focus { outline: none; border-color: #4299e1; }
textarea { resize: vertical; min-height: 65px; }

.btn { padding: 0.4rem 0.9rem; border: none; border-radius: 5px; cursor: pointer; font-size: 0.875rem; font-weight: 500; transition: opacity 0.15s; }
.btn:hover { opacity: 0.85; }
.btn-primary { background: #3182ce; color: white; }
.btn-success { background: #38a169; color: white; }
.btn-danger { background: #e53e3e; color: white; }
.btn-secondary { background: #718096; color: white; }
.btn-outline { background: white; color: #3182ce; border: 1px solid #3182ce; }
.btn-sm { padding: 0.25rem 0.6rem; font-size: 0.8rem; }
.btn-group { display: flex; gap: 0.4rem; flex-wrap: wrap; }

.badge {
  display: inline-block;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.badge-draft { background: #fefcbf; color: #975a16; }
.badge-published { background: #c6f6d5; color: #276749; }
.badge-cancelled { background: #fed7d7; color: #9b2c2c; }
.badge-finished { background: #e9d8fd; color: #553c9a; }
.badge-confirmed { background: #bee3f8; color: #2a4365; }

.error { color: #e53e3e; font-size: 0.82rem; margin-top: 0.25rem; }
.success { color: #38a169; font-size: 0.82rem; margin-top: 0.25rem; }
.empty { text-align: center; color: #a0aec0; padding: 2.5rem 1rem; font-size: 0.95rem; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1rem;
}
.modal {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  width: 100%;
  max-width: 460px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.modal-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem; color: #1a202c; }
.modal-footer { display: flex; gap: 0.5rem; margin-top: 1rem; justify-content: flex-end; }

.back-link { color: #3182ce; text-decoration: none; font-size: 0.875rem; display: inline-block; margin-bottom: 1rem; }
.back-link:hover { text-decoration: underline; }
</style>
