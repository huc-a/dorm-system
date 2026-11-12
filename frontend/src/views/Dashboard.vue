<template>
  <div>
    <div class="welcome">
      <div>
        <div class="w-title">{{ greeting }}，{{ auth.user ? auth.user.realName || auth.user.username : '' }}</div>
        <div class="w-sub">{{ todayText }} · 当前入住率 {{ stats.occupancyRate ?? '-' }}%，空闲床位 {{ stats.bedFree ?? '-' }} 个，待处理报修 {{ stats.repairPending ?? 0 }} 条</div>
      </div>
      <el-icon class="w-icon"><House /></el-icon>
    </div>
    <el-row :gutter="16">
      <el-col :span="6" v-for="c in cards" :key="c.label">
        <el-card shadow="hover" class="stat-card">
          <div style="display:flex;align-items:center;gap:15px">
            <span class="icon-chip" :style="{ background: c.bg, color: c.color }"><el-icon :size="24"><component :is="c.icon" /></el-icon></span>
            <div><div class="stat-value">{{ c.value }}</div><div class="stat-label">{{ c.label }}</div></div>
          </div>
          <div class="stat-bar"><span :style="{ width: c.pct + '%', background: c.color }"></span></div>
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
import { useAuthStore } from '../store/auth'
const stats = ref({})
const barEl = ref(null), pieEl = ref(null)
const cards = computed(() => [
  { label: '学生总数', value: stats.value.studentCount ?? '-', icon: 'User', color: '#2f7de1', bg: '#e8f2fd', pct: 100 },
  { label: '宿舍楼 / 房间', value: (stats.value.buildingCount ?? '-') + ' / ' + (stats.value.roomCount ?? '-'), icon: 'OfficeBuilding', color: '#21a675', bg: '#e4f6ef', pct: 100 },
  { label: '入住率', value: (stats.value.occupancyRate ?? '-') + '%', icon: 'Key', color: '#e8a13a', bg: '#fdf3e1', pct: stats.value.occupancyRate || 0 },
  { label: '待处理报修', value: stats.value.repairPending ?? '-', icon: 'Tools', color: '#ef6461', bg: '#fdecec', pct: Math.min(100, (stats.value.repairPending || 0) * 20) }
])
const auth = useAuthStore()
const greeting = computed(() => { const h = new Date().getHours(); return h < 6 ? '夜深了' : h < 12 ? '上午好' : h < 14 ? '中午好' : h < 18 ? '下午好' : '晚上好' })
const todayText = computed(() => {
  const d = new Date(); const wk = ['日', '一', '二', '三', '四', '五', '六'][d.getDay()]
  return `${d.getFullYear()} 年 ${d.getMonth() + 1} 月 ${d.getDate()} 日 · 星期${wk}`
})
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
      { name: '已入住', type: 'bar', data: by.map(b => b.used), itemStyle: { color: '#2f7de1', borderRadius: [5, 5, 0, 0] } },
      { name: '空闲', type: 'bar', data: by.map(b => b.free), itemStyle: { color: '#bcd8f8', borderRadius: [5, 5, 0, 0] } }
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
<style scoped>
.welcome {
  display: flex; justify-content: space-between; align-items: center;
  background: linear-gradient(100deg, #2564b4, #2f7de1 55%, #4a97e8);
  color: #fff; border-radius: 16px; padding: 22px 26px; margin-bottom: 16px;
  box-shadow: 0 12px 26px rgba(47, 125, 225, 0.28); overflow: hidden; position: relative;
}
.w-title { font-size: 21px; font-weight: 700; letter-spacing: 1px; }
.w-sub { margin-top: 6px; color: #cfe4fb; font-size: 13.5px; }
.w-icon { font-size: 92px; color: rgba(255, 255, 255, 0.16); margin-right: 6px; }
.icon-chip {
  width: 52px; height: 52px; border-radius: 14px; flex: none;
  display: inline-flex; align-items: center; justify-content: center;
}
.stat-value { font-size: 25px; font-weight: 800; color: #22364f; line-height: 1.15; }
.stat-label { color: #8496ab; font-size: 13px; margin-top: 2px; }
.stat-bar { height: 5px; background: #eef2f7; border-radius: 4px; margin-top: 14px; overflow: hidden; }
.stat-bar span { display: block; height: 100%; border-radius: 4px; transition: width .6s ease; }
</style>
