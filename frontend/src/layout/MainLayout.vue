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
