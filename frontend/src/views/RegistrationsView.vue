<template>
  <div>
    <h2>Mis Registros</h2>

    <p v-if="loading" class="empty">Cargando...</p>
    <p v-else-if="registrations.length === 0" class="empty">
      No tienes registros aún. Ve a <router-link to="/events">Eventos</router-link> para registrarte.
    </p>

    <div v-for="reg in registrations" :key="reg.id" class="card">
      <div class="card-body">
        <h3>{{ eventName(reg.event_id) }}</h3>
        <span :class="`badge badge-${reg.status}`">{{ reg.status }}</span>
        <p style="margin-top: 0.4rem;">Registrado el {{ fmt(reg.registered_at) }}</p>
        <p style="font-size: 0.78rem; color: #a0aec0;">ID evento: {{ reg.event_id }}</p>
      </div>
      <router-link :to="`/events/${reg.event_id}`" class="btn btn-outline btn-sm" style="align-self: flex-start;">
        Ver sesiones
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const registrations = ref([])
const eventNames = ref({})
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/register/')
    registrations.value = res.data
    await Promise.all(res.data.map(r => fetchEventName(r.event_id)))
  } finally {
    loading.value = false
  }
})

async function fetchEventName(eventId) {
  if (eventNames.value[eventId]) return
  try {
    const res = await api.get(`/events/${eventId}`)
    eventNames.value[eventId] = res.data.name
  } catch {
    eventNames.value[eventId] = 'Evento desconocido'
  }
}

function eventName(eventId) {
  return eventNames.value[eventId] || eventId
}

function fmt(dt) {
  return new Date(dt + 'Z').toLocaleString('es-CO', { dateStyle: 'long', timeStyle: 'short' })
}
</script>
