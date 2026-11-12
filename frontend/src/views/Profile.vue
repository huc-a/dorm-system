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
