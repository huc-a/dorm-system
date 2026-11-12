#!/usr/bin/env python3
# UI 美化改造：全局主题 / 主框架 / 登录页 / 仪表盘 / 列表状态标签
import os, textwrap
ROOT = os.path.expanduser("~/workspace/dorm-system/frontend")
def w(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("wrote", rel)

# ---------- 1. 全局主题 App.vue ----------
w("src/App.vue", r'''
<template><router-view /></template>
<style>
:root {
  --el-color-primary: #2f7de1;
  --el-color-primary-light-3: #6aa9ec;
  --el-color-primary-light-5: #9cc4f4;
  --el-color-primary-light-7: #c3dbf9;
  --el-color-primary-light-9: #eaf3fd;
  --el-color-primary-dark-2: #2564b4;
  --el-border-radius-base: 8px;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  background: #eef2f7;
  color: #303133;
  -webkit-font-smoothing: antialiased;
}
/* 卡片：圆角 + 柔和阴影 + 悬停浮起 */
.el-card {
  border: none !important;
  border-radius: 14px !important;
  box-shadow: 0 2px 12px rgba(31, 68, 120, 0.06) !important;
  transition: box-shadow .25s ease, transform .25s ease;
}
.el-card.is-hover-shadow:hover {
  box-shadow: 0 10px 28px rgba(31, 68, 120, 0.14) !important;
  transform: translateY(-3px);
}
.el-card__header { border-bottom: 1px solid #eef2f7 !important; font-weight: 600; }
/* 表格：表头浅蓝底、行悬停高亮、圆角外框 */
.el-table { border-radius: 10px; overflow: hidden; }
.el-table th.el-table__cell {
  background: linear-gradient(180deg, #f2f7fd, #e8f1fb) !important;
  color: #33506e; font-weight: 600;
}
.el-table .el-table__row:hover > td.el-table__cell { background: #f2f8ff !important; }
/* 按钮与输入 */
.el-button { border-radius: 8px !important; font-weight: 500; }
.el-button--primary {
  background: linear-gradient(135deg, #3a8dde, #2f7de1) !important;
  border-color: transparent !important;
  box-shadow: 0 4px 12px rgba(47, 125, 225, 0.28);
}
.el-button--primary:hover { filter: brightness(1.07); }
.el-input__wrapper, .el-select__wrapper { border-radius: 8px !important; }
/* 对话框与分页 */
.el-dialog { border-radius: 16px !important; overflow: hidden; }
.el-dialog__header { background: linear-gradient(90deg, #f2f7fd, #ffffff); margin-right: 0 !important; padding: 18px 24px !important; }
.el-dialog__body { padding: 22px 24px 8px !important; }
.el-pagination .el-pager li { border-radius: 6px; }
.el-pagination .el-pager li.is-active { background: linear-gradient(135deg, #3a8dde, #2f7de1); }
/* 侧栏菜单：胶囊式选中态 */
.el-menu { padding: 8px 10px; }
.el-menu .el-menu-item { border-radius: 10px; margin: 3px 0; height: 46px; line-height: 46px; }
.el-menu .el-menu-item:hover { background: rgba(255, 255, 255, 0.08) !important; color: #fff !important; }
.el-menu .el-menu-item.is-active {
  background: linear-gradient(90deg, #2f7de1, #4a97e8) !important;
  color: #fff !important;
  box-shadow: 0 4px 12px rgba(47, 125, 225, 0.35);
}
/* 滚动条 */
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-thumb { background: #c3cedb; border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: #a7b7ca; }
::-webkit-scrollbar-track { background: transparent; }
.el-main { padding: 20px 22px !important; }
.el-tag { border-radius: 6px; font-weight: 500; }
</style>
''')

# ---------- 2. 主框架 MainLayout.vue ----------
w("src/layout/MainLayout.vue", r'''
<template>
  <el-container style="height:100vh">
    <el-aside width="224px" class="sidebar">
      <div class="brand">
        <div class="brand-logo"><el-icon :size="20"><House /></el-icon></div>
        <div>
          <div class="brand-name">宿舍管理系统</div>
          <div class="brand-sub">DORMITORY SYSTEM</div>
        </div>
      </div>
      <el-menu :default-active="$route.path" router background-color="transparent" text-color="#aebfd4" active-text-color="#ffffff" style="border:0">
        <el-menu-item index="/dashboard"><el-icon><DataBoard /></el-icon>首页概览</el-menu-item>
        <template v-if="!auth.isStudent">
          <el-menu-item index="/students"><el-icon><User /></el-icon>学生管理</el-menu-item>
          <el-menu-item index="/buildings"><el-icon><OfficeBuilding /></el-icon>宿舍楼管理</el-menu-item>
          <el-menu-item index="/rooms"><el-icon><Grid /></el-icon>房间管理</el-menu-item>
          <el-menu-item index="/beds"><el-icon><Files /></el-icon>床位管理</el-menu-item>
          <el-menu-item index="/checkins"><el-icon><Key /></el-icon>入住管理</el-menu-item>
          <el-menu-item index="/repairs"><el-icon><Tools /></el-icon>报修管理</el-menu-item>
          <el-menu-item index="/hygiene"><el-icon><Brush /></el-icon>卫生检查</el-menu-item>
          <el-menu-item index="/visitors"><el-icon><Avatar /></el-icon>访客登记</el-menu-item>
          <el-menu-item index="/fees"><el-icon><Money /></el-icon>水电费管理</el-menu-item>
          <el-menu-item index="/leaves"><el-icon><Calendar /></el-icon>请假/晚归审批</el-menu-item>
          <el-menu-item index="/notices"><el-icon><Bell /></el-icon>公告管理</el-menu-item>
          <el-menu-item v-if="auth.isAdmin" index="/users"><el-icon><Setting /></el-icon>系统账号</el-menu-item>
        </template>
        <template v-else>
          <el-menu-item index="/my-dorm"><el-icon><House /></el-icon>我的宿舍</el-menu-item>
          <el-menu-item index="/notice-list"><el-icon><Bell /></el-icon>通知公告</el-menu-item>
        </template>
        <el-menu-item index="/profile"><el-icon><UserFilled /></el-icon>个人中心</el-menu-item>
      </el-menu>
      <div class="sidebar-footer">毕业设计 · Spring Boot + Vue</div>
    </el-aside>
    <el-container>
      <el-header class="topbar">
        <div class="topbar-title">
          <span class="crumb-home">宿舍管理系统</span>
          <el-icon class="crumb-sep"><ArrowRight /></el-icon>
          <span class="crumb-cur">{{ $route.meta.title || '' }}</span>
        </div>
        <el-dropdown @command="cmd">
          <span class="user-chip">
            <span class="avatar">{{ avatarText }}</span>
            <span>{{ auth.user ? auth.user.realName || auth.user.username : '' }}</span>
            <el-tag size="small" effect="light">{{ roleName }}</el-tag>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main><router-view :key="$route.fullPath" /></el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
const auth = useAuthStore()
const router = useRouter()
const roleName = computed(() => ({ ADMIN: '管理员', DORM_MANAGER: '宿舍管理员', STUDENT: '学生' }[auth.role] || auth.role))
const avatarText = computed(() => {
  const n = auth.user ? (auth.user.realName || auth.user.username || '?') : '?'
  return n.slice(0, 1)
})
function cmd(c) {
  if (c === 'logout') { auth.logout(); router.push('/login') }
  if (c === 'profile') router.push('/profile')
}
</script>
<style scoped>
.sidebar {
  background: linear-gradient(180deg, #22364f 0%, #2b4361 55%, #243a55 100%);
  color: #fff; display: flex; flex-direction: column;
  box-shadow: 4px 0 18px rgba(20, 42, 70, 0.18); z-index: 5;
}
.brand { display: flex; align-items: center; gap: 12px; padding: 20px 18px 16px; border-bottom: 1px solid rgba(255,255,255,0.09); }
.brand-logo {
  width: 40px; height: 40px; border-radius: 11px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #3a8dde, #2f7de1); box-shadow: 0 6px 14px rgba(47,125,225,.45); color: #fff;
}
.brand-name { font-size: 16.5px; font-weight: 700; letter-spacing: 1px; }
.brand-sub { font-size: 9.5px; color: #7e97b5; letter-spacing: 2.2px; margin-top: 2px; }
.sidebar-footer { margin-top: auto; padding: 14px 18px; font-size: 11.5px; color: #637d99; border-top: 1px solid rgba(255,255,255,0.07); }
.topbar {
  background: rgba(255,255,255,0.92); backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 2px 12px rgba(31,68,120,0.07); height: 58px !important; z-index: 4;
}
.topbar-title { display: flex; align-items: center; gap: 8px; font-size: 15px; }
.crumb-home { color: #8496ab; }
.crumb-sep { color: #c0cedd; font-size: 13px; }
.crumb-cur { font-weight: 700; color: #22364f; }
.user-chip { display: flex; align-items: center; gap: 9px; cursor: pointer; outline: none; }
.avatar {
  width: 34px; height: 34px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #3a8dde, #2564b4); color: #fff; font-weight: 700; font-size: 15px;
  box-shadow: 0 4px 10px rgba(47,125,225,.35);
}
</style>
''')

# ---------- 3. 登录页 Login.vue ----------
w("src/views/Login.vue", r'''
<template>
  <div class="login-bg">
    <div class="login-shell">
      <div class="brand-panel">
        <div class="bp-logo"><el-icon :size="26"><House /></el-icon></div>
        <h1>宿舍管理系统</h1>
        <p class="bp-en">DORMITORY MANAGEMENT SYSTEM</p>
        <ul class="bp-points">
          <li><el-icon><CircleCheck /></el-icon>入住分配 · 调宿退宿 · 床位校验</li>
          <li><el-icon><CircleCheck /></el-icon>在线报修 · 卫生检查 · 访客登记</li>
          <li><el-icon><CircleCheck /></el-icon>水电费用 · 请假审批 · 数据统计</li>
        </ul>
        <div class="bp-foot">基于 Spring Boot + Vue 的毕业设计</div>
      </div>
      <el-card class="login-card">
        <h2>欢迎登录</h2>
        <p class="sub">请输入账号与密码进入系统</p>
        <el-form :model="form" @keyup.enter="submit">
          <el-form-item><el-input v-model="form.username" placeholder="用户名 / 学号" prefix-icon="User" size="large" /></el-form-item>
          <el-form-item><el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password /></el-form-item>
          <el-button type="primary" size="large" class="login-btn" :loading="loading" @click="submit">登 录</el-button>
        </el-form>
        <div class="demo-box">
          <div>演示账号：admin / admin123（管理员）</div>
          <div>宿管：manager / manager123</div>
          <div>学生：20230101 / 123456</div>
        </div>
        <div style="text-align:center;margin-top:14px">
          <el-link type="primary" @click="$router.push('/register')">学生自助注册 →</el-link>
        </div>
      </el-card>
    </div>
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
.login-bg {
  min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px;
  background:
    radial-gradient(900px 480px at 15% 10%, rgba(84, 169, 255, .5), transparent 60%),
    radial-gradient(800px 500px at 88% 90%, rgba(38, 198, 218, .35), transparent 60%),
    linear-gradient(135deg, #173a5e, #1d4e89 45%, #2f7de1);
}
.login-shell {
  display: flex; width: 880px; max-width: 94vw; border-radius: 22px; overflow: hidden;
  box-shadow: 0 30px 70px rgba(8, 30, 58, .45);
  animation: rise .5s ease both;
}
@keyframes rise { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }
.brand-panel {
  flex: 1.05; padding: 44px 38px; color: #fff; position: relative;
  background: linear-gradient(160deg, rgba(18, 46, 82, .55), rgba(23, 66, 116, .25));
  backdrop-filter: blur(2px);
}
.bp-logo {
  width: 54px; height: 54px; border-radius: 15px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #3a8dde, #2f7de1); box-shadow: 0 10px 22px rgba(47,125,225,.5);
}
.brand-panel h1 { font-size: 29px; margin: 22px 0 6px; letter-spacing: 2px; }
.bp-en { color: #9dc2ec; letter-spacing: 3px; font-size: 11px; margin: 0 0 30px; }
.bp-points { list-style: none; padding: 0; margin: 0; display: grid; gap: 15px; color: #d9e9fb; font-size: 14.5px; }
.bp-points .el-icon { color: #5fd08a; margin-right: 9px; vertical-align: -2px; }
.bp-foot { position: absolute; left: 38px; bottom: 30px; color: #7fa5cf; font-size: 12.5px; }
.login-card { flex: 1; border-radius: 0 !important; padding: 34px 36px 26px; box-shadow: none !important; }
.login-card h2 { margin: 4px 0 6px; font-size: 23px; color: #22364f; }
.login-card .sub { color: #909399; margin: 0 0 24px; font-size: 13.5px; }
.login-btn { width: 100%; height: 46px; font-size: 16px; letter-spacing: 6px; }
.demo-box {
  margin-top: 20px; background: #f2f7fd; border: 1px dashed #c9def6; border-radius: 10px;
  padding: 11px 14px; font-size: 12.5px; color: #5b7a9e; line-height: 1.9;
}
@media (max-width: 760px) { .brand-panel { display: none; } }
</style>
''')
print("BEAUTIFY PART 1 DONE")
