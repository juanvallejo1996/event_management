<template>
  <div>
    <h2>Gestión de Usuarios</h2>

    <div class="search-card">
      <p class="section-label">Buscar usuario por email</p>
      <div class="search-row">
        <input v-model="email" type="email" placeholder="usuario@ejemplo.com" @keyup.enter="search" />
        <button class="btn btn-primary" @click="search" :disabled="!email.trim()">Buscar</button>
      </div>
      <p class="error" v-if="searchError">{{ searchError }}</p>
    </div>

    <div v-if="result" class="user-result">
      <div class="user-profile-card">
        <div class="profile-avatar">{{ initials }}</div>
        <div class="profile-info">
          <h3>{{ result.name }}</h3>
          <p class="profile-email">{{ result.email }}</p>
          <span :class="`badge badge-role-${result.role}`">{{ roleLabel(result.role) }}</span>
        </div>
      </div>

      <div class="action-section">
        <p class="section-label">Cambiar rol del usuario</p>
        <p class="section-hint">El rol determina qué acciones puede realizar el usuario en el sistema.</p>
        <div class="role-selector">
          <label class="role-option" v-for="r in roles" :key="r.value">
            <input type="radio" v-model="newRole" :value="r.value" />
            <div :class="['role-card', { selected: newRole === r.value }]">
              <span class="role-name">{{ r.label }}</span>
              <span class="role-desc">{{ r.desc }}</span>
            </div>
          </label>
        </div>
        <button
          class="btn btn-primary"
          @click="changeRole"
          :disabled="newRole === result.role"
        >
          Guardar nuevo rol
        </button>
        <p class="success" v-if="actionSuccess">{{ actionSuccess }}</p>
        <p class="error" v-if="actionError">{{ actionError }}</p>
      </div>

      <div class="danger-section">
        <p class="section-label danger-label">Zona de peligro</p>
        <div class="danger-row">
          <div>
            <p class="danger-title">Eliminar usuario</p>
            <p class="danger-hint">Esta acción es permanente y no se puede deshacer.</p>
          </div>
          <button class="btn btn-danger" @click="deleteUser">Eliminar usuario</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../services/api'

const email = ref('')
const result = ref(null)
const newRole = ref('attendee')
const searchError = ref('')
const actionSuccess = ref('')
const actionError = ref('')

const roles = [
  { value: 'attendee', label: 'Attendee', desc: 'Puede registrarse a eventos y ver información.' },
  { value: 'organizer', label: 'Organizer', desc: 'Puede crear, editar y eliminar eventos y sesiones.' },
  { value: 'admin', label: 'Admin', desc: 'Acceso total, incluyendo gestión de usuarios.' },
]

const initials = computed(() => {
  const name = result.value?.name || ''
  return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase() || '?'
})

function roleLabel(role) {
  return roles.find(r => r.value === role)?.label || role
}

async function search() {
  searchError.value = ''
  result.value = null
  actionSuccess.value = ''
  actionError.value = ''
  try {
    const res = await api.get(`/users/search/${encodeURIComponent(email.value.trim())}`)
    result.value = res.data
    newRole.value = res.data.role
  } catch (e) {
    searchError.value = e.response?.data?.detail || 'Usuario no encontrado'
  }
}

async function changeRole() {
  actionSuccess.value = ''
  actionError.value = ''
  try {
    const res = await api.patch(`/users/${result.value.id}/role`, { role: newRole.value })
    result.value = res.data
    newRole.value = res.data.role
    actionSuccess.value = 'Rol actualizado correctamente'
  } catch (e) {
    actionError.value = e.response?.data?.detail || 'Error al cambiar el rol'
  }
}

async function deleteUser() {
  if (!confirm(`¿Eliminar permanentemente a ${result.value.name}?`)) return
  actionSuccess.value = ''
  actionError.value = ''
  try {
    await api.delete(`/users/${result.value.id}`)
    result.value = null
    email.value = ''
  } catch (e) {
    actionError.value = e.response?.data?.detail || 'Error al eliminar el usuario'
  }
}
</script>

<style scoped>
.search-card {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1.25rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.section-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #4a5568;
  margin-bottom: 0.6rem;
}

.user-result { display: flex; flex-direction: column; gap: 1rem; }

.user-profile-card {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  gap: 1.1rem;
}
.profile-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #4299e1;
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.profile-info h3 { font-size: 1.05rem; color: #1a202c; margin-bottom: 0.15rem; }
.profile-email { font-size: 0.875rem; color: #718096; margin-bottom: 0.4rem; }

.badge-role-admin    { background: #fed7d7; color: #9b2c2c; display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }
.badge-role-organizer { background: #c6f6d5; color: #276749; display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }
.badge-role-attendee  { background: #bee3f8; color: #2a4365; display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }

.action-section {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.section-hint { font-size: 0.82rem; color: #718096; margin-bottom: 1rem; }

.role-selector {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}
.role-option { cursor: pointer; }
.role-option input[type="radio"] { display: none; }
.role-card {
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.65rem 1rem;
  min-width: 140px;
  transition: all 0.15s;
  user-select: none;
}
.role-card:hover { border-color: #90cdf4; }
.role-card.selected { border-color: #3182ce; background: #ebf8ff; }
.role-name { display: block; font-weight: 700; font-size: 0.875rem; color: #2d3748; margin-bottom: 0.2rem; }
.role-desc { display: block; font-size: 0.75rem; color: #718096; }

.danger-section {
  background: white;
  border: 1px solid #fed7d7;
  border-radius: 8px;
  padding: 1.25rem;
}
.danger-label { color: #c53030; }
.danger-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; margin-top: 0.5rem; }
.danger-title { font-size: 0.9rem; font-weight: 600; color: #2d3748; margin-bottom: 0.2rem; }
.danger-hint { font-size: 0.82rem; color: #718096; }
</style>
