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
.login-bg { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(120deg, rgba(11,30,56,.52), rgba(11,30,56,.18) 55%, rgba(11,30,56,.42)), url('/login-wallpaper.jpg') center / cover no-repeat, #173a5e; padding: 24px 0; }
.login-card { width: 440px; padding: 14px; border-radius: 18px !important; }
</style>
