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
