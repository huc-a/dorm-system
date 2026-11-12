import { defineStore } from 'pinia'
import request from '../utils/request'
export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('dorm_token') || '',
    user: JSON.parse(localStorage.getItem('dorm_user') || 'null'),
    student: JSON.parse(localStorage.getItem('dorm_student') || 'null')
  }),
  getters: {
    role: s => (s.user ? s.user.role : ''),
    isStudent: s => s.user && s.user.role === 'STUDENT',
    isAdmin: s => s.user && s.user.role === 'ADMIN'
  },
  actions: {
    async login(username, password) {
      const res = await request.post('/auth/login', { username, password })
      this.token = res.data.token
      this.user = res.data.user
      localStorage.setItem('dorm_token', this.token)
      localStorage.setItem('dorm_user', JSON.stringify(this.user))
      await this.fetchMe()
      return this.user
    },
    async fetchMe() {
      try {
        const res = await request.get('/auth/me')
        this.user = res.data.user
        this.student = res.data.student && res.data.student.id ? res.data.student : null
        localStorage.setItem('dorm_user', JSON.stringify(this.user))
        localStorage.setItem('dorm_student', JSON.stringify(this.student))
      } catch (e) { /* ignore */ }
    },
    logout() {
      this.token = ''; this.user = null; this.student = null
      localStorage.removeItem('dorm_token'); localStorage.removeItem('dorm_user'); localStorage.removeItem('dorm_student')
    }
  }
})
