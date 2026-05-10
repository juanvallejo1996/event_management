import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import EventsView from '../views/EventsView.vue'
import EventDetailView from '../views/EventDetailView.vue'
import RegistrationsView from '../views/RegistrationsView.vue'
import UsersView from '../views/UsersView.vue'

const routes = [
  { path: '/login', component: LoginView },
  { path: '/', redirect: '/events' },
  { path: '/events', component: EventsView, meta: { requiresAuth: true } },
  { path: '/events/:id', component: EventDetailView, meta: { requiresAuth: true } },
  { path: '/registrations', component: RegistrationsView, meta: { requiresAuth: true } },
  { path: '/users', component: UsersView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) next('/login')
  else if (to.path === '/login' && token) next('/events')
  else next()
})

export default router
