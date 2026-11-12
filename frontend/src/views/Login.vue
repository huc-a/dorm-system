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
    linear-gradient(120deg, rgba(11, 30, 56, .52), rgba(11, 30, 56, .18) 55%, rgba(11, 30, 56, .42)),
    url('/login-wallpaper.jpg') center / cover no-repeat,
    #173a5e;
}
.login-shell {
  display: flex; width: 880px; max-width: 94vw; border-radius: 22px; overflow: hidden;
  box-shadow: 0 30px 70px rgba(8, 30, 58, .45);
  animation: rise .5s ease both;
}
@keyframes rise { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }
.brand-panel {
  flex: 1.05; padding: 44px 38px; color: #fff; position: relative;
  background: linear-gradient(160deg, rgba(13, 36, 66, .72), rgba(18, 52, 92, .45));
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
