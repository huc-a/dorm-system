#!/usr/bin/env python3
import os, textwrap
ROOT = os.path.expanduser("~/workspace/dorm-system/frontend")
def w(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("wrote", rel)

w("src/router/index.js", r'''
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
''')

w("src/views/Login.vue", r'''
<template>
  <div class="login-bg">
    <el-card class="login-card">
      <h2 style="text-align:center;margin:6px 0 4px">宿舍管理系统</h2>
      <p style="text-align:center;color:#909399;margin:0 0 20px">Dormitory Management System</p>
      <el-form :model="form" @keyup.enter="submit">
        <el-form-item><el-input v-model="form.username" placeholder="用户名 / 学号" prefix-icon="User" size="large" /></el-form-item>
        <el-form-item><el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password /></el-form-item>
        <el-button type="primary" size="large" style="width:100%" :loading="loading" @click="submit">登 录</el-button>
      </el-form>
      <div style="display:flex;justify-content:space-between;margin-top:14px;font-size:13px">
        <span style="color:#909399">演示账号：admin / admin123<br/>宿管：manager / manager123<br/>学生：20230101 / 123456</span>
        <el-link type="primary" @click="$router.push('/register')">学生注册</el-link>
      </div>
    </el-card>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../store/auth'
const router = useRouter(), auth = useAuthStore()
const form = ref({ username: '', password: '' }), loading = ref(false)
async function submit() {
  if (!form.value.username || !form.value.password) return ElMessage.warning('请输入用户名和密码')
  loading.value = true
  try { await auth.login(form.value.username, form.value.password); ElMessage.success('登录成功'); router.push('/dashboard') }
  catch (e) { /* 拦截器已提示 */ } finally { loading.value = false }
}
</script>
<style scoped>
.login-bg { height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1d4e89, #409eff 60%, #79bbff); }
.login-card { width: 400px; padding: 16px 12px; border-radius: 12px; }
</style>
''')

w("src/views/Register.vue", r'''
<template>
  <div class="login-bg">
    <el-card class="login-card">
      <h2 style="text-align:center;margin:6px 0 18px">学生注册</h2>
      <el-form :model="form" label-width="76px">
        <el-form-item label="学号"><el-input v-model="form.studentNo" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-form-item label="性别"><el-select v-model="form.gender" style="width:100%"><el-option label="男" value="男" /><el-option label="女" value="女" /></el-select></el-form-item>
        <el-form-item label="学院"><el-input v-model="form.college" /></el-form-item>
        <el-form-item label="专业"><el-input v-model="form.major" /></el-form-item>
        <el-form-item label="班级"><el-input v-model="form.className" /></el-form-item>
        <el-form-item label="年级"><el-input v-model="form.grade" placeholder="如 2023级" /></el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-button type="primary" style="width:100%" @click="submit">注 册</el-button>
        <div style="text-align:center;margin-top:12px"><el-link @click="$router.push('/login')">已有账号，去登录</el-link></div>
      </el-form>
    </el-card>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../utils/request'
const router = useRouter()
const form = ref({ studentNo: '', name: '', password: '', gender: '男', college: '', major: '', className: '', grade: '', phone: '' })
async function submit() {
  if (!form.value.studentNo || !form.value.name || !form.value.password) return ElMessage.warning('学号、姓名、密码必填')
  await request.post('/auth/register', form.value)
  ElMessage.success('注册成功，请用学号登录')
  router.push('/login')
}
</script>
<style scoped>
.login-bg { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1d4e89, #409eff 60%, #79bbff); padding: 24px 0; }
.login-card { width: 440px; padding: 10px; border-radius: 12px; }
</style>
''')

w("src/views/Dashboard.vue", r'''
<template>
  <div>
    <el-row :gutter="16">
      <el-col :span="6" v-for="c in cards" :key="c.label">
        <el-card shadow="hover" class="stat-card">
          <div style="display:flex;align-items:center;gap:14px">
            <el-icon :size="34" :color="c.color"><component :is="c.icon" /></el-icon>
            <div><div style="font-size:24px;font-weight:bold">{{ c.value }}</div><div style="color:#909399">{{ c.label }}</div></div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="12"><el-card shadow="never"><template #header>各楼栋入住情况</template><div ref="barEl" style="height:320px"></div></el-card></el-col>
      <el-col :span="12"><el-card shadow="never"><template #header>床位使用 / 报修状态</template><div ref="pieEl" style="height:320px"></div></el-card></el-col>
    </el-row>
    <el-card shadow="never" style="margin-top:16px">
      <template #header>最新公告</template>
      <el-timeline>
        <el-timeline-item v-for="n in stats.latestNotices || []" :key="n.id" :timestamp="(n.publishTime || '').replace('T', ' ').slice(0, 16)" placement="top">
          <el-tag v-if="n.top" type="danger" size="small">置顶</el-tag>
          <b style="margin-left:6px">{{ n.title }}</b>
          <div style="color:#606266;margin-top:4px">{{ n.content }}</div>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>
<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '../utils/request'
const stats = ref({})
const barEl = ref(null), pieEl = ref(null)
const cards = computed(() => [
  { label: '学生总数', value: stats.value.studentCount ?? '-', icon: 'User', color: '#409eff' },
  { label: '宿舍楼 / 房间', value: (stats.value.buildingCount ?? '-') + ' / ' + (stats.value.roomCount ?? '-'), icon: 'OfficeBuilding', color: '#67c23a' },
  { label: '入住率', value: (stats.value.occupancyRate ?? '-') + '%', icon: 'Key', color: '#e6a23c' },
  { label: '待处理报修', value: stats.value.repairPending ?? '-', icon: 'Tools', color: '#f56c6c' }
])
onMounted(async () => {
  const res = await request.get('/dashboard/stats')
  stats.value = res.data
  await nextTick()
  const by = stats.value.byBuilding || []
  echarts.init(barEl.value).setOption({
    tooltip: {}, legend: { data: ['已入住', '空闲'] },
    xAxis: { type: 'category', data: by.map(b => b.building) },
    yAxis: { type: 'value' },
    series: [
      { name: '已入住', type: 'bar', data: by.map(b => b.used), itemStyle: { color: '#409eff' } },
      { name: '空闲', type: 'bar', data: by.map(b => b.free), itemStyle: { color: '#a0cfff' } }
    ]
  })
  echarts.init(pieEl.value).setOption({
    tooltip: {}, legend: { bottom: 0 },
    series: [{ type: 'pie', radius: ['40%', '68%'], data: [
      { name: '已入住床位', value: stats.value.bedUsed || 0 },
      { name: '空闲床位', value: stats.value.bedFree || 0 },
      { name: '待处理报修', value: stats.value.repairPending || 0 },
      { name: '处理中报修', value: stats.value.repairProcessing || 0 }
    ] }]
  })
})
</script>
<style scoped>.stat-card { border-radius: 10px; }</style>
''')

w("src/views/MyDorm.vue", r'''
<template>
  <div>
    <el-row :gutter="16">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>我的住宿信息</template>
          <el-descriptions v-if="my" :column="1" border>
            <el-descriptions-item label="学生">{{ my.student ? my.student.name : '-' }}（{{ my.student ? my.student.studentNo : '' }}）</el-descriptions-item>
            <el-descriptions-item label="宿舍">{{ my.room && my.room.building ? my.room.building.name : '' }} {{ my.room ? my.room.roomNo : '-' }} 房 {{ my.bed ? my.bed.bedNo : '' }}</el-descriptions-item>
            <el-descriptions-item label="入住日期">{{ my.checkInDate }}</el-descriptions-item>
            <el-descriptions-item label="状态">{{ my.status }}</el-descriptions-item>
          </el-descriptions>
          <el-empty v-else description="尚未分配宿舍，请联系宿管员" />
        </el-card>
        <el-card shadow="never" style="margin-top:16px">
          <template #header>我的水电费</template>
          <el-table :data="myFees" border size="small">
            <el-table-column prop="period" label="账期" /><el-table-column prop="electricityUsage" label="用电(度)" />
            <el-table-column prop="waterUsage" label="用水(吨)" /><el-table-column prop="totalAmount" label="金额(元)" />
            <el-table-column prop="status" label="状态" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>我要报修</template>
          <el-form :model="repairForm" label-width="80px">
            <el-form-item label="标题"><el-input v-model="repairForm.title" /></el-form-item>
            <el-form-item label="类别"><el-select v-model="repairForm.category" style="width:100%"><el-option v-for="o in ['水电','家具','门窗','网络','其他']" :key="o" :label="o" :value="o" /></el-select></el-form-item>
            <el-form-item label="优先级"><el-select v-model="repairForm.priority" style="width:100%"><el-option v-for="o in ['低','普通','高','紧急']" :key="o" :label="o" :value="o" /></el-select></el-form-item>
            <el-form-item label="描述"><el-input v-model="repairForm.description" type="textarea" :rows="3" /></el-form-item>
            <el-button type="primary" @click="submitRepair">提交报修</el-button>
          </el-form>
        </el-card>
        <el-card shadow="never" style="margin-top:16px">
          <template #header>请假 / 晚归申请</template>
          <el-form :model="leaveForm" label-width="80px">
            <el-form-item label="类型"><el-select v-model="leaveForm.type" style="width:100%"><el-option label="请假离校" value="请假离校" /><el-option label="晚归" value="晚归" /></el-select></el-form-item>
            <el-form-item label="开始"><el-date-picker v-model="leaveForm.startTime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width:100%" /></el-form-item>
            <el-form-item label="结束"><el-date-picker v-model="leaveForm.endTime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width:100%" /></el-form-item>
            <el-form-item label="事由"><el-input v-model="leaveForm.reason" type="textarea" :rows="2" /></el-form-item>
            <el-button type="primary" @click="submitLeave">提交申请</el-button>
          </el-form>
          <el-table :data="myLeaves" border size="small" style="margin-top:12px">
            <el-table-column prop="type" label="类型" /><el-table-column prop="reason" label="事由" />
            <el-table-column prop="status" label="状态" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    <el-card shadow="never" style="margin-top:16px">
      <template #header>我的报修记录</template>
      <el-table :data="myRepairs" border>
        <el-table-column prop="title" label="标题" /><el-table-column prop="category" label="类别" width="80" />
        <el-table-column prop="priority" label="优先级" width="80" /><el-table-column prop="status" label="状态" width="90" />
        <el-table-column prop="repairer" label="维修人" width="100" /><el-table-column prop="result" label="处理结果" />
        <el-table-column prop="createTime" label="报修时间" width="160" />
      </el-table>
    </el-card>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../utils/request'
import { useAuthStore } from '../store/auth'
const auth = useAuthStore()
const my = ref(null), myRepairs = ref([]), myFees = ref([]), myLeaves = ref([])
const repairForm = ref({ title: '', category: '水电', priority: '普通', description: '' })
const leaveForm = ref({ type: '请假离校', startTime: '', endTime: '', reason: '' })
async function load() {
  const stu = auth.student
  if (!stu) return
  const ci = await request.get('/checkins/my/' + stu.id)
  my.value = ci.data
  const all = await request.get('/repairs/all')
  myRepairs.value = (all.data || []).filter(r => r.student && r.student.id === stu.id)
  const leaves = await request.get('/leaves/all')
  myLeaves.value = (leaves.data || []).filter(r => r.student && r.student.id === stu.id)
  if (my.value && my.value.room) {
    const fees = await request.get('/fees/all')
    myFees.value = (fees.data || []).filter(f => f.room && f.room.id === my.value.room.id)
  }
}
async function submitRepair() {
  if (!repairForm.value.title) return ElMessage.warning('请填写报修标题')
  const stu = auth.student
  await request.post('/repairs', { ...repairForm.value, status: '待处理', student: stu ? { id: stu.id } : null, room: my.value && my.value.room ? { id: my.value.room.id } : null })
  ElMessage.success('报修已提交'); repairForm.value = { title: '', category: '水电', priority: '普通', description: '' }; load()
}
async function submitLeave() {
  const stu = auth.student
  await request.post('/leaves', { ...leaveForm.value, status: '待审批', student: stu ? { id: stu.id } : null })
  ElMessage.success('申请已提交'); load()
}
onMounted(async () => { await auth.fetchMe(); load() })
</script>
''')

w("src/views/NoticeList.vue", r'''
<template>
  <el-card shadow="never">
    <el-timeline>
      <el-timeline-item v-for="n in list" :key="n.id" :timestamp="(n.publishTime || '').replace('T', ' ').slice(0, 16)" placement="top">
        <el-tag size="small">{{ n.type }}</el-tag>
        <el-tag v-if="n.top" type="danger" size="small" style="margin-left:6px">置顶</el-tag>
        <h4 style="margin:8px 0 4px">{{ n.title }}</h4>
        <div style="color:#606266;white-space:pre-wrap">{{ n.content }}</div>
        <div style="color:#909399;font-size:12px;margin-top:4px">发布：{{ n.publisher }}</div>
      </el-timeline-item>
    </el-timeline>
    <el-empty v-if="!list.length" description="暂无公告" />
  </el-card>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import request from '../utils/request'
const list = ref([])
onMounted(async () => { const res = await request.get('/notices/all'); list.value = res.data || [] })
</script>
''')

w("src/views/Users.vue", r'''
<template>
  <el-card shadow="never">
    <div style="margin-bottom:16px"><el-button type="primary" plain @click="openCreate">+ 新增账号</el-button></div>
    <el-table :data="rows" border stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="realName" label="姓名" />
      <el-table-column label="角色" width="120"><template #default="{ row }">{{ { ADMIN: '管理员', DORM_MANAGER: '宿舍管理员', STUDENT: '学生' }[row.role] || row.role }}</template></el-table-column>
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column label="状态" width="80"><template #default="{ row }">{{ row.status === 0 ? '禁用' : '启用' }}</template></el-table-column>
      <el-table-column label="操作" width="240">
        <template #default="{ row }">
          <el-button size="small" @click="toggle(row)">{{ row.status === 0 ? '启用' : '禁用' }}</el-button>
          <el-button size="small" type="warning" @click="reset(row)">重置密码</el-button>
          <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="dialog" title="新增账号" width="480px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" placeholder="默认 123456" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.realName" /></el-form-item>
        <el-form-item label="角色"><el-select v-model="form.role" style="width:100%">
          <el-option label="管理员" value="ADMIN" /><el-option label="宿舍管理员" value="DORM_MANAGER" /><el-option label="学生" value="STUDENT" />
        </el-select></el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialog = false">取消</el-button><el-button type="primary" @click="save">保存</el-button></template>
    </el-dialog>
  </el-card>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../utils/request'
const rows = ref([]), dialog = ref(false)
const form = ref({ username: '', password: '', realName: '', role: 'DORM_MANAGER', phone: '', email: '' })
async function load() { const res = await request.get('/users'); rows.value = res.data || [] }
function openCreate() { form.value = { username: '', password: '', realName: '', role: 'DORM_MANAGER', phone: '', email: '' }; dialog.value = true }
async function save() { await request.post('/users', { ...form.value, status: 1 }); ElMessage.success('创建成功'); dialog.value = false; load() }
async function toggle(row) { await request.put('/users/' + row.id, { ...row, status: row.status === 0 ? 1 : 0 }); load() }
async function reset(row) { await ElMessageBox.confirm('将密码重置为 123456？', '提示'); await request.post('/users/' + row.id + '/reset-password'); ElMessage.success('已重置') }
async function remove(row) { await ElMessageBox.confirm('确认删除该账号？', '提示', { type: 'warning' }); await request.delete('/users/' + row.id); load() }
onMounted(load)
</script>
''')

w("src/views/Profile.vue", r'''
<template>
  <el-row :gutter="16">
    <el-col :span="10">
      <el-card shadow="never">
        <template #header>账号信息</template>
        <el-descriptions :column="1" border v-if="auth.user">
          <el-descriptions-item label="用户名">{{ auth.user.username }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ auth.user.realName }}</el-descriptions-item>
          <el-descriptions-item label="角色">{{ { ADMIN: '管理员', DORM_MANAGER: '宿舍管理员', STUDENT: '学生' }[auth.user.role] }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ auth.user.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ auth.user.email || '-' }}</el-descriptions-item>
        </el-descriptions>
        <el-descriptions :column="1" border v-if="auth.student" style="margin-top:16px">
          <el-descriptions-item label="学号">{{ auth.student.studentNo }}</el-descriptions-item>
          <el-descriptions-item label="学院/专业">{{ auth.student.college }} / {{ auth.student.major }}</el-descriptions-item>
          <el-descriptions-item label="班级">{{ auth.student.className }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
    </el-col>
    <el-col :span="10">
      <el-card shadow="never">
        <template #header>修改密码</template>
        <el-form :model="form" label-width="90px">
          <el-form-item label="原密码"><el-input v-model="form.oldPassword" type="password" show-password /></el-form-item>
          <el-form-item label="新密码"><el-input v-model="form.newPassword" type="password" show-password /></el-form-item>
          <el-form-item label="确认密码"><el-input v-model="confirm" type="password" show-password /></el-form-item>
          <el-button type="primary" @click="submit">确认修改</el-button>
        </el-form>
      </el-card>
    </el-col>
  </el-row>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../utils/request'
import { useAuthStore } from '../store/auth'
const auth = useAuthStore()
const form = ref({ oldPassword: '', newPassword: '' }), confirm = ref('')
async function submit() {
  if (form.value.newPassword !== confirm.value) return ElMessage.warning('两次新密码不一致')
  if (form.value.newPassword.length < 6) return ElMessage.warning('新密码至少 6 位')
  await request.post('/auth/change-password', form.value)
  ElMessage.success('密码修改成功')
  form.value = { oldPassword: '', newPassword: '' }; confirm.value = ''
}
onMounted(() => auth.fetchMe())
</script>
''')
print("FRONT PART C DONE")
