<template>
  <div>
    <router-link to="/events" class="back-link">← Volver a eventos</router-link>

    <div v-if="event" class="card" style="margin-bottom: 1.5rem;">
      <div class="card-body">
        <h2 style="margin-bottom: 0.3rem;">{{ event.name }}</h2>
        <span :class="`badge badge-${event.status}`">{{ event.status }}</span>
        <p style="margin-top: 0.5rem;">{{ event.description }}</p>
        <p>Capacidad: {{ event.capacity }}</p>
        <p>{{ fmt(event.starts_at) }} → {{ fmt(event.ends_at) }}</p>
      </div>
    </div>

    <div class="row">
      <h2>Sesiones</h2>
      <button v-if="canManage" class="btn btn-primary" @click="openCreate">+ Crear sesión</button>
    </div>

    <p v-if="loading" class="empty">Cargando sesiones...</p>
    <p v-else-if="sessions.length === 0" class="empty">Este evento no tiene sesiones aún.</p>

    <div v-for="session in sessions" :key="session.id" class="card">
      <div class="card-body">
        <h3>{{ session.title }}</h3>
        <p>{{ session.description }}</p>
        <p><strong>Speaker:</strong> {{ session.speaker_name }} — {{ session.speaker_bio }}</p>
        <p>Capacidad: {{ session.capacity }} &nbsp;|&nbsp; {{ fmt(session.starts_at) }} → {{ fmt(session.ends_at) }}</p>
      </div>
      <div v-if="canManage" class="btn-group" style="flex-direction: column; align-items: flex-end;">
        <button class="btn btn-secondary btn-sm" @click="openEdit(session)">Editar</button>
        <button class="btn btn-danger btn-sm" @click="deleteSession(session.id)">Eliminar</button>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <p class="modal-title">{{ editing ? 'Editar sesión' : 'Crear sesión' }}</p>
        <form @submit.prevent="saveSession">
          <label>Título</label>
          <input v-model="form.title" required />
          <label>Descripción</label>
          <textarea v-model="form.description" required></textarea>
          <label>Nombre del speaker</label>
          <input v-model="form.speaker_name" required />
          <label>Bio del speaker</label>
          <textarea v-model="form.speaker_bio" required></textarea>
          <label>Capacidad</label>
          <input v-model.number="form.capacity" type="number" min="1" required />
          <label>Inicio</label>
          <input v-model="form.starts_at" type="datetime-local" required />
          <label>Fin</label>
          <input v-model="form.ends_at" type="datetime-local" required />
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
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const eventId = route.params.id

const event = ref(null)
const sessions = ref([])
const loading = ref(false)
const showModal = ref(false)
const editing = ref(null)
const formError = ref('')

const emptyForm = () => ({
  title: '', description: '', speaker_name: '', speaker_bio: '',
  capacity: 10, starts_at: '', ends_at: '',
})
const form = ref(emptyForm())

const user = computed(() => {
  const u = localStorage.getItem('user')
  return u ? JSON.parse(u) : null
})
const canManage = computed(() => ['admin', 'organizer'].includes(user.value?.role))

onMounted(async () => {
  const [evRes] = await Promise.all([
    api.get(`/events/${eventId}`),
    loadSessions(),
  ])
  event.value = evRes.data
})

async function loadSessions() {
  loading.value = true
  try {
    const res = await api.get(`/events/${eventId}/sessions/`)
    sessions.value = res.data
  } finally {
    loading.value = false
  }
}

function fmt(dt) {
  return new Date(dt + 'Z').toLocaleString('es-CO', { dateStyle: 'medium', timeStyle: 'short' })
}

function toLocalInput(dt) {
  return new Date(dt + 'Z').toISOString().slice(0, 16)
}

function openCreate() {
  editing.value = null
  form.value = emptyForm()
  formError.value = ''
  showModal.value = true
}

function openEdit(session) {
  editing.value = session.id
  form.value = {
    title: session.title,
    description: session.description,
    speaker_name: session.speaker_name,
    speaker_bio: session.speaker_bio,
    capacity: session.capacity,
    starts_at: toLocalInput(session.starts_at),
    ends_at: toLocalInput(session.ends_at),
  }
  formError.value = ''
  showModal.value = true
}

async function saveSession() {
  formError.value = ''
  try {
    const payload = {
      ...form.value,
      starts_at: new Date(form.value.starts_at).toISOString(),
      ends_at: new Date(form.value.ends_at).toISOString(),
    }
    if (editing.value) {
      await api.put(`/events/${eventId}/sessions/${editing.value}`, payload)
    } else {
      await api.post(`/events/${eventId}/sessions/`, payload)
    }
    showModal.value = false
    await loadSessions()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Error al guardar la sesión'
  }
}

async function deleteSession(sessionId) {
  if (!confirm('¿Eliminar esta sesión?')) return
  try {
    await api.delete(`/events/${eventId}/sessions/${sessionId}`)
    await loadSessions()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al eliminar')
  }
}
</script>
