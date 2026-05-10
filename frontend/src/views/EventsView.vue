<template>
  <div>
    <div class="row">
      <h2>Eventos</h2>
      <button v-if="canManage" class="btn btn-primary" @click="openCreate">+ Crear evento</button>
    </div>

    <div class="search-row">
      <input v-model="searchTerm" placeholder="Buscar por nombre..." @keyup.enter="search" />
      <button class="btn btn-secondary" @click="search">Buscar</button>
      <button class="btn btn-outline" @click="loadAll">Ver todos</button>
    </div>

    <p v-if="loading" class="empty">Cargando...</p>
    <p v-else-if="events.length === 0" class="empty">No se encontraron eventos.</p>

    <div v-for="event in events" :key="event.id" class="card">
      <div class="card-body">
        <h3>{{ event.name }}</h3>
        <span :class="`badge badge-${event.status}`">{{ event.status }}</span>
        <p style="margin-top: 0.4rem;">{{ event.description }}</p>
        <div class="event-dates">
          <span class="date-item"><span class="date-label">Inicio</span> {{ fmt(event.starts_at) }}</span>
          <span class="date-sep">→</span>
          <span class="date-item"><span class="date-label">Fin</span> {{ fmt(event.ends_at) }}</span>
        </div>
        <p>Capacidad: {{ event.capacity }}</p>
      </div>
      <div class="btn-group" style="flex-direction: column; align-items: flex-end;">
        <router-link :to="`/events/${event.id}`" class="btn btn-outline btn-sm">Sesiones</router-link>
        <button class="btn btn-success btn-sm" @click="registerToEvent(event.id)">Registrarme</button>
        <template v-if="canManage">
          <button class="btn btn-secondary btn-sm" @click="openEdit(event)">Editar</button>
          <button class="btn btn-danger btn-sm" @click="deleteEvent(event.id)">Eliminar</button>
        </template>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <p class="modal-title">{{ editing ? 'Editar evento' : 'Crear evento' }}</p>
        <form @submit.prevent="saveEvent">
          <label>Nombre</label>
          <input v-model="form.name" required />
          <label>Descripción</label>
          <textarea v-model="form.description" required></textarea>
          <label>Capacidad</label>
          <input v-model.number="form.capacity" type="number" min="1" required />
          <label>Fecha de inicio</label>
          <input v-model="form.starts_at" type="datetime-local" required />
          <label>Fecha de fin</label>
          <input v-model="form.ends_at" type="datetime-local" required />
          <template v-if="editing">
            <label>Estado</label>
            <select v-model="form.status">
              <option value="draft">Borrador</option>
              <option value="published">Publicado</option>
              <option value="cancelled">Cancelado</option>
              <option value="finished">Finalizado</option>
            </select>
          </template>
          <p class="error" v-if="formError">{{ formError }}</p>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showModal = false">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const events = ref([])
const searchTerm = ref('')
const loading = ref(false)
const showModal = ref(false)
const editing = ref(null)
const formError = ref('')

const emptyForm = () => ({ name: '', description: '', capacity: 10, starts_at: '', ends_at: '', status: 'draft' })
const form = ref(emptyForm())

const user = computed(() => {
  const u = localStorage.getItem('user')
  return u ? JSON.parse(u) : null
})
const canManage = computed(() => ['admin', 'organizer'].includes(user.value?.role))

onMounted(loadAll)

async function loadAll() {
  loading.value = true
  try {
    const res = await api.get('/events/')
    events.value = res.data
  } catch {
    events.value = []
  } finally {
    loading.value = false
  }
}

async function search() {
  const term = searchTerm.value.trim()
  if (!term) return loadAll()
  loading.value = true
  try {
    const res = await api.get(`/events/search/${encodeURIComponent(term)}`)
    events.value = res.data
  } catch {
    events.value = []
  } finally {
    loading.value = false
  }
}

function fmt(dt) {
  return new Date(dt + 'Z').toLocaleString('es-CO', { dateStyle: 'medium', timeStyle: 'short' })
}

function toLocalInput(dt) {
  const d = new Date(dt + 'Z')
  return d.toISOString().slice(0, 16)
}

function openCreate() {
  editing.value = null
  form.value = emptyForm()
  formError.value = ''
  showModal.value = true
}

function openEdit(event) {
  editing.value = event.id
  form.value = {
    name: event.name,
    description: event.description,
    capacity: event.capacity,
    starts_at: toLocalInput(event.starts_at),
    ends_at: toLocalInput(event.ends_at),
    status: event.status,
  }
  formError.value = ''
  showModal.value = true
}

async function saveEvent() {
  formError.value = ''
  try {
    const payload = {
      ...form.value,
      starts_at: new Date(form.value.starts_at).toISOString(),
      ends_at: new Date(form.value.ends_at).toISOString(),
    }
    if (editing.value) {
      await api.put(`/events/${editing.value}`, payload)
    } else {
      await api.post('/events/', payload)
    }
    showModal.value = false
    await loadAll()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Error al guardar el evento'
  }
}

async function deleteEvent(id) {
  if (!confirm('¿Eliminar este evento?')) return
  try {
    await api.delete(`/events/${id}`)
    await loadAll()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al eliminar')
  }
}

async function registerToEvent(eventId) {
  try {
    await api.post('/register/', { event_id: eventId })
    alert('Registro exitoso')
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al registrarse')
  }
}
</script>

<style scoped>
.event-dates {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 0.4rem 0 0.2rem;
  flex-wrap: wrap;
}
.date-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.875rem;
  color: #4a5568;
}
.date-label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #a0aec0;
}
.date-sep { color: #cbd5e0; font-size: 1rem; }
</style>
