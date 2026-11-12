#!/usr/bin/env python3
import os, textwrap
ROOT = os.path.expanduser("~/workspace/dorm-system/frontend")
def w(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("wrote", rel)

w("package.json", r'''
{
  "name": "dorm-system-frontend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": { "dev": "vite", "build": "vite build", "preview": "vite preview" },
  "dependencies": {
    "@element-plus/icons-vue": "^2.3.1",
    "axios": "^1.7.7",
    "echarts": "^5.5.1",
    "element-plus": "^2.8.6",
    "pinia": "^2.2.4",
    "vue": "^3.5.12",
    "vue-router": "^4.4.5"
  },
  "devDependencies": { "@vitejs/plugin-vue": "^5.1.4", "vite": "^5.4.10" }
}
''')

w("vite.config.js", r'''
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5174,
    proxy: { '/api': { target: 'http://127.0.0.1:8081', changeOrigin: true } }
  }
})
''')

w("index.html", r'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>宿舍管理系统</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
''')

w("src/main.js", r'''
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) app.component(key, component)
app.use(createPinia()).use(router).use(ElementPlus)
app.mount('#app')
''')

w("src/App.vue", r'''
<template><router-view /></template>
<style>
body { margin: 0; font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif; background: #f5f7fa; }
</style>
''')

w("src/utils/request.js", r'''
import axios from 'axios'
import { ElMessage } from 'element-plus'
const request = axios.create({ baseURL: '/api', timeout: 15000 })
request.interceptors.request.use(cfg => {
  const token = localStorage.getItem('dorm_token')
  if (token) cfg.headers.Authorization = 'Bearer ' + token
  return cfg
})
request.interceptors.response.use(
  res => {
    const data = res.data
    if (data && typeof data.code === 'number' && data.code !== 200) {
      ElMessage.error(data.msg || '请求失败')
      return Promise.reject(new Error(data.msg || '请求失败'))
    }
    return data
  },
  err => {
    if (err.response && err.response.status === 403) ElMessage.error('无权访问')
    else if (err.response && err.response.status === 401) { localStorage.removeItem('dorm_token'); location.hash = '#/login' }
    else ElMessage.error(err.message || '网络错误')
    return Promise.reject(err)
  }
)
export default request
''')

w("src/store/auth.js", r'''
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
''')

w("src/config/modules.js", r'''
// 各业务模块的表格列与表单字段配置，驱动通用 CRUD 页面
const genderOpts = ['男', '女']
export const modules = {
  students: {
    title: '学生管理', endpoint: '/students', searchKey: 'name', searchPlaceholder: '按姓名搜索',
    columns: [
      { prop: 'studentNo', label: '学号', width: 110 }, { prop: 'name', label: '姓名', width: 90 },
      { prop: 'gender', label: '性别', width: 60 }, { prop: 'college', label: '学院' },
      { prop: 'major', label: '专业' }, { prop: 'className', label: '班级', width: 110 },
      { prop: 'grade', label: '年级', width: 90 }, { prop: 'phone', label: '电话', width: 120 },
      { prop: 'status', label: '状态', width: 80 }
    ],
    fields: [
      { prop: 'studentNo', label: '学号', required: true }, { prop: 'name', label: '姓名', required: true },
      { prop: 'gender', label: '性别', type: 'select', options: genderOpts },
      { prop: 'college', label: '学院' }, { prop: 'major', label: '专业' },
      { prop: 'className', label: '班级' }, { prop: 'grade', label: '年级' },
      { prop: 'phone', label: '电话' }, { prop: 'email', label: '邮箱' },
      { prop: 'idCard', label: '身份证号' }, { prop: 'homeAddress', label: '家庭住址' },
      { prop: 'status', label: '状态', type: 'select', options: ['在读', '毕业', '休学'] }
    ]
  },
  buildings: {
    title: '宿舍楼管理', endpoint: '/buildings', searchKey: 'name', searchPlaceholder: '按楼名搜索',
    columns: [
      { prop: 'code', label: '楼栋编号', width: 100 }, { prop: 'name', label: '楼栋名称' },
      { prop: 'floors', label: '楼层数', width: 80 }, { prop: 'genderType', label: '类型', width: 110 },
      { prop: 'managerName', label: '宿管员', width: 100 }, { prop: 'managerPhone', label: '宿管电话', width: 120 },
      { prop: 'address', label: '地址' }
    ],
    fields: [
      { prop: 'code', label: '楼栋编号', required: true }, { prop: 'name', label: '楼栋名称', required: true },
      { prop: 'floors', label: '楼层数', type: 'number' },
      { prop: 'genderType', label: '类型', type: 'select', options: ['男生宿舍', '女生宿舍', '混合宿舍'] },
      { prop: 'managerName', label: '宿管员' }, { prop: 'managerPhone', label: '宿管电话' },
      { prop: 'address', label: '地址' }, { prop: 'remark', label: '备注', type: 'textarea' }
    ]
  },
  rooms: {
    title: '房间管理', endpoint: '/rooms', searchKey: 'roomNo', searchPlaceholder: '按房号搜索',
    columns: [
      { prop: 'building.name', label: '所属楼栋' }, { prop: 'roomNo', label: '房号', width: 80 },
      { prop: 'floor', label: '楼层', width: 70 }, { prop: 'roomType', label: '房型', width: 90 },
      { prop: 'capacity', label: '床位数', width: 80 }, { prop: 'gender', label: '性别', width: 60 },
      { prop: 'facilities', label: '设施' }, { prop: 'status', label: '状态', width: 90 }
    ],
    fields: [
      { prop: 'building', label: '所属楼栋', type: 'fk', endpoint: '/buildings/all', optionLabel: e => e.name, required: true },
      { prop: 'roomNo', label: '房号', required: true }, { prop: 'floor', label: '楼层', type: 'number' },
      { prop: 'capacity', label: '床位数', type: 'number' },
      { prop: 'roomType', label: '房型', type: 'select', options: ['四人间', '六人间', '八人间'] },
      { prop: 'gender', label: '性别', type: 'select', options: genderOpts },
      { prop: 'facilities', label: '设施' },
      { prop: 'status', label: '状态', type: 'select', options: ['正常', '维修中', '停用'] },
      { prop: 'remark', label: '备注', type: 'textarea' }
    ]
  },
  beds: {
    title: '床位管理', endpoint: '/beds', searchKey: 'bedNo', searchPlaceholder: '按床号搜索',
    columns: [
      { prop: 'room.building.name', label: '楼栋' }, { prop: 'room.roomNo', label: '房号', width: 80 },
      { prop: 'bedNo', label: '床号', width: 90 }, { prop: 'status', label: '状态', width: 90 },
      { prop: 'student.name', label: '入住学生' }, { prop: 'student.studentNo', label: '学号', width: 110 }
    ],
    fields: [
      { prop: 'room', label: '所属房间', type: 'fk', endpoint: '/rooms/all', optionLabel: e => (e.building ? e.building.name + ' ' : '') + e.roomNo, required: true },
      { prop: 'bedNo', label: '床号', required: true },
      { prop: 'status', label: '状态', type: 'select', options: ['空闲', '已入住', '维修'] },
      { prop: 'student', label: '入住学生', type: 'fk', endpoint: '/students/all', optionLabel: e => e.name + '（' + e.studentNo + '）' }
    ]
  },
  checkins: {
    title: '入住管理', endpoint: '/checkins', searchKey: 'status', searchPlaceholder: '按状态搜索（在住/已退宿）',
    columns: [
      { prop: 'student.name', label: '学生' }, { prop: 'student.studentNo', label: '学号', width: 110 },
      { prop: 'room.building.name', label: '楼栋' }, { prop: 'room.roomNo', label: '房号', width: 80 },
      { prop: 'bed.bedNo', label: '床号', width: 90 }, { prop: 'checkInDate', label: '入住日期', width: 110 },
      { prop: 'checkOutDate', label: '退宿日期', width: 110 }, { prop: 'status', label: '状态', width: 90 }
    ],
    fields: [
      { prop: 'student', label: '学生', type: 'fk', endpoint: '/students/all', optionLabel: e => e.name + '（' + e.studentNo + '）' },
      { prop: 'room', label: '房间', type: 'fk', endpoint: '/rooms/all', optionLabel: e => (e.building ? e.building.name + ' ' : '') + e.roomNo },
      { prop: 'bed', label: '床位', type: 'fk', endpoint: '/beds/all', optionLabel: e => (e.room ? e.room.roomNo + ' ' : '') + e.bedNo + '（' + e.status + '）' },
      { prop: 'checkInDate', label: '入住日期', type: 'date' }, { prop: 'checkOutDate', label: '退宿日期', type: 'date' },
      { prop: 'status', label: '状态', type: 'select', options: ['在住', '已退宿'] },
      { prop: 'remark', label: '备注', type: 'textarea' }
    ],
    rowActions: [
      { label: '退宿', type: 'warning', show: row => row.status === '在住', method: 'post', url: row => '/checkins/' + row.id + '/checkout', confirm: '确认办理退宿？床位将被释放。' }
    ]
  },
  repairs: {
    title: '报修管理', endpoint: '/repairs', searchKey: 'title', searchPlaceholder: '按标题搜索',
    columns: [
      { prop: 'title', label: '报修标题' }, { prop: 'category', label: '类别', width: 80 },
      { prop: 'student.name', label: '报修学生', width: 100 }, { prop: 'room.roomNo', label: '房号', width: 80 },
      { prop: 'priority', label: '优先级', width: 80 }, { prop: 'status', label: '状态', width: 90 },
      { prop: 'repairer', label: '维修人', width: 90 }, { prop: 'createTime', label: '报修时间', width: 160 }
    ],
    fields: [
      { prop: 'title', label: '报修标题', required: true },
      { prop: 'student', label: '报修学生', type: 'fk', endpoint: '/students/all', optionLabel: e => e.name + '（' + e.studentNo + '）' },
      { prop: 'room', label: '房间', type: 'fk', endpoint: '/rooms/all', optionLabel: e => (e.building ? e.building.name + ' ' : '') + e.roomNo },
      { prop: 'category', label: '类别', type: 'select', options: ['水电', '家具', '门窗', '网络', '其他'] },
      { prop: 'priority', label: '优先级', type: 'select', options: ['低', '普通', '高', '紧急'] },
      { prop: 'status', label: '状态', type: 'select', options: ['待处理', '处理中', '已完成', '已关闭'] },
      { prop: 'repairer', label: '维修人' },
      { prop: 'description', label: '问题描述', type: 'textarea' }, { prop: 'result', label: '处理结果', type: 'textarea' }
    ]
  },
  hygiene: {
    title: '卫生检查', endpoint: '/hygiene', searchKey: 'grade', searchPlaceholder: '按等级搜索（优秀/良好/合格/不合格）',
    columns: [
      { prop: 'room.building.name', label: '楼栋' }, { prop: 'room.roomNo', label: '房号', width: 80 },
      { prop: 'inspector', label: '检查人', width: 100 }, { prop: 'checkDate', label: '检查日期', width: 110 },
      { prop: 'score', label: '总分', width: 70 }, { prop: 'grade', label: '等级', width: 80 },
      { prop: 'remark', label: '备注' }
    ],
    fields: [
      { prop: 'room', label: '房间', type: 'fk', endpoint: '/rooms/all', optionLabel: e => (e.building ? e.building.name + ' ' : '') + e.roomNo, required: true },
      { prop: 'inspector', label: '检查人' }, { prop: 'checkDate', label: '检查日期', type: 'date' },
      { prop: 'score', label: '总分', type: 'number' },
      { prop: 'grade', label: '等级', type: 'select', options: ['优秀', '良好', '合格', '不合格'] },
      { prop: 'groundScore', label: '地面分', type: 'number' }, { prop: 'bedScore', label: '床铺分', type: 'number' },
      { prop: 'deskScore', label: '桌面分', type: 'number' }, { prop: 'bathroomScore', label: '卫生间分', type: 'number' },
      { prop: 'remark', label: '备注', type: 'textarea' }
    ]
  },
  visitors: {
    title: '访客登记', endpoint: '/visitors', searchKey: 'visitorName', searchPlaceholder: '按访客姓名搜索',
    columns: [
      { prop: 'visitorName', label: '访客姓名', width: 100 }, { prop: 'visitorPhone', label: '访客电话', width: 120 },
      { prop: 'visitedStudent.name', label: '被访学生', width: 100 }, { prop: 'room.roomNo', label: '房号', width: 80 },
      { prop: 'visitTime', label: '来访时间', width: 160 }, { prop: 'leaveTime', label: '离开时间', width: 160 },
      { prop: 'reason', label: '来访事由' }, { prop: 'status', label: '状态', width: 80 }
    ],
    fields: [
      { prop: 'visitorName', label: '访客姓名', required: true }, { prop: 'visitorPhone', label: '访客电话' },
      { prop: 'idCard', label: '身份证号' },
      { prop: 'visitedStudent', label: '被访学生', type: 'fk', endpoint: '/students/all', optionLabel: e => e.name + '（' + e.studentNo + '）' },
      { prop: 'room', label: '房间', type: 'fk', endpoint: '/rooms/all', optionLabel: e => (e.building ? e.building.name + ' ' : '') + e.roomNo },
      { prop: 'visitTime', label: '来访时间', type: 'datetime' }, { prop: 'leaveTime', label: '离开时间', type: 'datetime' },
      { prop: 'reason', label: '来访事由' },
      { prop: 'status', label: '状态', type: 'select', options: ['在访', '已离开'] }
    ]
  },
  fees: {
    title: '水电费管理', endpoint: '/fees', searchKey: 'period', searchPlaceholder: '按账期搜索（如 2026-10）',
    columns: [
      { prop: 'room.building.name', label: '楼栋' }, { prop: 'room.roomNo', label: '房号', width: 80 },
      { prop: 'period', label: '账期', width: 90 }, { prop: 'electricityUsage', label: '用电(度)', width: 90 },
      { prop: 'waterUsage', label: '用水(吨)', width: 90 }, { prop: 'totalAmount', label: '总金额(元)', width: 100 },
      { prop: 'status', label: '缴费状态', width: 90 }, { prop: 'dueDate', label: '缴费截止', width: 110 }
    ],
    fields: [
      { prop: 'room', label: '房间', type: 'fk', endpoint: '/rooms/all', optionLabel: e => (e.building ? e.building.name + ' ' : '') + e.roomNo, required: true },
      { prop: 'period', label: '账期' }, { prop: 'electricityUsage', label: '用电(度)', type: 'number' },
      { prop: 'waterUsage', label: '用水(吨)', type: 'number' }, { prop: 'electricityFee', label: '电费(元)', type: 'number' },
      { prop: 'waterFee', label: '水费(元)', type: 'number' }, { prop: 'totalAmount', label: '总金额(元)', type: 'number' },
      { prop: 'status', label: '缴费状态', type: 'select', options: ['未缴费', '已缴费'] },
      { prop: 'dueDate', label: '缴费截止', type: 'date' }
    ]
  },
  leaves: {
    title: '请假/晚归审批', endpoint: '/leaves', searchKey: 'status', searchPlaceholder: '按状态搜索（待审批/已批准/已驳回）',
    columns: [
      { prop: 'student.name', label: '学生' }, { prop: 'type', label: '类型', width: 100 },
      { prop: 'startTime', label: '开始时间', width: 160 }, { prop: 'endTime', label: '结束时间', width: 160 },
      { prop: 'reason', label: '事由' }, { prop: 'status', label: '状态', width: 90 },
      { prop: 'approver', label: '审批人', width: 90 }
    ],
    fields: [
      { prop: 'student', label: '学生', type: 'fk', endpoint: '/students/all', optionLabel: e => e.name + '（' + e.studentNo + '）' },
      { prop: 'type', label: '类型', type: 'select', options: ['请假离校', '晚归'] },
      { prop: 'startTime', label: '开始时间', type: 'datetime' }, { prop: 'endTime', label: '结束时间', type: 'datetime' },
      { prop: 'reason', label: '事由', type: 'textarea' },
      { prop: 'status', label: '状态', type: 'select', options: ['待审批', '已批准', '已驳回'] },
      { prop: 'approver', label: '审批人' }, { prop: 'approveRemark', label: '审批意见', type: 'textarea' }
    ]
  },
  notices: {
    title: '公告管理', endpoint: '/notices', searchKey: 'title', searchPlaceholder: '按标题搜索',
    columns: [
      { prop: 'title', label: '标题' }, { prop: 'type', label: '类型', width: 110 },
      { prop: 'publisher', label: '发布人', width: 100 }, { prop: 'publishTime', label: '发布时间', width: 160 },
      { prop: 'top', label: '置顶', width: 70 }
    ],
    fields: [
      { prop: 'title', label: '标题', required: true },
      { prop: 'type', label: '类型', type: 'select', options: ['系统公告', '宿舍通知', '卫生通报', '停水停电'] },
      { prop: 'publisher', label: '发布人' },
      { prop: 'top', label: '是否置顶', type: 'switch' },
      { prop: 'content', label: '内容', type: 'textarea' }
    ]
  }
}
''')
print("FRONT PART A DONE")
