<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h1>Event Management</h1>

      <div class="tabs">
        <button :class="['tab', { active: mode === 'login' }]" @click="switchMode('login')">Iniciar sesión</button>
        <button :class="['tab', { active: mode === 'register' }]" @click="switchMode('register')">Crear cuenta</button>
      </div>

      <form v-if="mode === 'login'" @submit.prevent="login">
        <label>Email</label>
        <input v-model="loginForm.email" type="email" required placeholder="admin@example.com" autocomplete="email" />
        <label>Contraseña</label>
        <input v-model="loginForm.password" type="password" required placeholder="••••••••" autocomplete="current-password" />
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Ingresar' }}
        </button>
        <p class="error" v-if="error">{{ error }}</p>
      </form>

      <form v-else @submit.prevent="register">
        <label>Nombre</label>
        <input v-model="registerForm.name" required placeholder="Tu nombre completo" />
        <label>Email</label>
        <input v-model="registerForm.email" type="email" required placeholder="tu@email.com" autocomplete="email" />
        <label>Contraseña</label>
        <input v-model="registerForm.password" type="password" required placeholder="••••••••" autocomplete="new-password" minlength="6" />
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
        </button>
        <p class="error" v-if="error">{{ error }}</p>
        <p class="success" v-if="success">{{ success }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const mode = ref('login')
const loading = ref(false)
const error = ref('')
const success = ref('')

const loginForm = ref({ email: '', password: '' })
const registerForm = ref({ name: '', email: '', password: '' })

function switchMode(m) {
  mode.value = m
  error.value = ''
  success.value = ''
}

async function login() {
  error.value = ''
  loading.value = true
  try {
    const res = await api.post('/users/login', {
      email: loginForm.value.email,
      password: loginForm.value.password,
    })
    localStorage.setItem('token', res.data.access_token)
    const me = await api.get(`/users/search/${encodeURIComponent(loginForm.value.email)}`)
    localStorage.setItem('user', JSON.stringify(me.data))
    router.push('/events')
  } catch {
    error.value = 'Email o contraseña incorrectos'
  } finally {
    loading.value = false
  }
}

async function register() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await api.post('/users/', {
      name: registerForm.value.name,
      email: registerForm.value.email,
      password: registerForm.value.password,
    })
    success.value = 'Cuenta creada. Ahora puedes iniciar sesión.'
    loginForm.value.email = registerForm.value.email
    registerForm.value = { name: '', email: '', password: '' }
    setTimeout(() => switchMode('login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear la cuenta'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: calc(100vh - 52px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}
.login-card {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  width: 100%;
  max-width: 390px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
h1 { font-size: 1.4rem; color: #1a202c; margin-bottom: 1rem; }

.tabs {
  display: flex;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 1.25rem;
}
.tab {
  flex: 1;
  background: none;
  border: none;
  padding: 0.5rem;
  font-size: 0.9rem;
  color: #718096;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.15s;
}
.tab.active {
  color: #3182ce;
  border-bottom-color: #3182ce;
  font-weight: 600;
}
form { display: flex; flex-direction: column; gap: 0.4rem; }
.btn { width: 100%; padding: 0.55rem; font-size: 0.95rem; margin-top: 0.5rem; }
</style>
