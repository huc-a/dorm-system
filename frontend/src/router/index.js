import { createRouter, createWebHashHistory } from 'vue-router'
import MainLayout from '../layout/MainLayout.vue'
import { modules } from '../config/modules'
import CrudPage from '../components/CrudPage.vue'

const moduleRoutes = Object.entries(modules).map(([key, cfg]) => ({
  path: '/' + key, name: key,
  component: CrudPage, props: { config: key === 'checkins' ? { ...cfg, assignApi: true } : cfg },
  meta: { title: cfg.title }
}))
const routes = [
  { path: '/login', component: () => import('../views/Login.vue'), meta: { title: '登录' } },
  { path: '/register', component: () => import('../views/Register.vue'), meta: { title: '学生注册' } },
  {
    path: '/', component: MainLayout, redirect: '/dashboard',
    children: [
      { path: 'dashboard', component: () => import('../views/Dashboard.vue'), meta: { title: '首页概览' } },
      ...moduleRoutes.map(r => ({ ...r, path: r.path.slice(1) })),
      { path: 'users', component: () => import('../views/Users.vue'), meta: { title: '系统账号' } },
      { path: 'my-dorm', component: () => import('../views/MyDorm.vue'), meta: { title: '我的宿舍' } },
      { path: 'notice-list', component: () => import('../views/NoticeList.vue'), meta: { title: '通知公告' } },
      { path: 'profile', component: () => import('../views/Profile.vue'), meta: { title: '个人中心' } }
    ]
  }
]
const router = createRouter({ history: createWebHashHistory(), routes })
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('dorm_token')
  if (to.path !== '/login' && to.path !== '/register' && !token) next('/login')
  else next()
})
export default router
