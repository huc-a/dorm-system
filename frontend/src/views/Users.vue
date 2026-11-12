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
