#!/usr/bin/env python3
import os, textwrap
ROOT = os.path.expanduser("~/workspace/dorm-system/frontend")
def w(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("wrote", rel)
def patch(rel, old, new):
    p = os.path.join(ROOT, rel)
    s = open(p, encoding="utf-8").read()
    assert old in s, f"PATCH TARGET NOT FOUND in {rel}: {old[:60]}"
    open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
    print("patched", rel)

# ---------- Dashboard：欢迎横幅 + 图标徽章统计卡 + 图表配色 ----------
s = open(os.path.join(ROOT, "src/views/Dashboard.vue"), encoding="utf-8").read()
old_tpl = """<template>
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
    </el-row>"""
new_tpl = """<template>
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
    </el-row>"""
assert old_tpl in s; s = s.replace(old_tpl, new_tpl, 1)

old_cards = """const cards = computed(() => [
  { label: '学生总数', value: stats.value.studentCount ?? '-', icon: 'User', color: '#409eff' },
  { label: '宿舍楼 / 房间', value: (stats.value.buildingCount ?? '-') + ' / ' + (stats.value.roomCount ?? '-'), icon: 'OfficeBuilding', color: '#67c23a' },
  { label: '入住率', value: (stats.value.occupancyRate ?? '-') + '%', icon: 'Key', color: '#e6a23c' },
  { label: '待处理报修', value: stats.value.repairPending ?? '-', icon: 'Tools', color: '#f56c6c' }
])"""
new_cards = """const cards = computed(() => [
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
})"""
assert old_cards in s; s = s.replace(old_cards, new_cards, 1)
s = s.replace("import request from '../utils/request'",
              "import request from '../utils/request'\nimport { useAuthStore } from '../store/auth'", 1)
s = s.replace("{ name: '已入住', type: 'bar', data: by.map(b => b.used), itemStyle: { color: '#409eff' } },",
              "{ name: '已入住', type: 'bar', data: by.map(b => b.used), itemStyle: { color: '#2f7de1', borderRadius: [5, 5, 0, 0] } },", 1)
s = s.replace("{ name: '空闲', type: 'bar', data: by.map(b => b.free), itemStyle: { color: '#a0cfff' } }",
              "{ name: '空闲', type: 'bar', data: by.map(b => b.free), itemStyle: { color: '#bcd8f8', borderRadius: [5, 5, 0, 0] } }", 1)
old_style = "<style scoped>.stat-card { border-radius: 10px; }</style>"
new_style = """<style scoped>
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
</style>"""
assert old_style in s; s = s.replace(old_style, new_style, 1)
open(os.path.join(ROOT, "src/views/Dashboard.vue"), "w", encoding="utf-8").write(s)
print("patched Dashboard.vue")

# ---------- CrudPage：页头标题 + 状态标签 ----------
patch("src/components/CrudPage.vue",
"""    <el-card shadow="never">
      <div style="display:flex;gap:12px;margin-bottom:16px;align-items:center">""",
"""    <el-card shadow="never">
      <div class="page-head">
        <div class="page-title">{{ config.title }}</div>
        <div class="page-count">共 {{ total }} 条记录</div>
      </div>
      <div style="display:flex;gap:12px;margin-bottom:16px;align-items:center">""")

patch("src/components/CrudPage.vue",
"""        <el-table-column v-for="c in config.columns" :key="c.prop" :label="c.label" :width="c.width" show-overflow-tooltip>
          <template #default="{ row }">{{ display(row, c.prop) }}</template>
        </el-table-column>""",
"""        <el-table-column v-for="c in config.columns" :key="c.prop" :label="c.label" :width="c.width" show-overflow-tooltip>
          <template #default="{ row }">
            <el-tag v-if="tagType(c.prop, display(row, c.prop))" :type="tagType(c.prop, display(row, c.prop))" effect="light" size="small">{{ display(row, c.prop) }}</el-tag>
            <span v-else>{{ display(row, c.prop) }}</span>
          </template>
        </el-table-column>""")

patch("src/components/CrudPage.vue",
"""function display(row, prop) {""",
"""const TAG_MAP = {
  '在住': 'success', '已退宿': 'info', '空闲': 'success', '已入住': '', '维修': 'warning', '维修中': 'warning',
  '停用': 'danger', '正常': 'success', '待处理': 'danger', '处理中': 'warning', '已完成': 'success', '已关闭': 'info',
  '待审批': 'warning', '已批准': 'success', '已驳回': 'danger', '未缴费': 'danger', '已缴费': 'success',
  '在访': '', '已离开': 'info', '在读': 'success', '毕业': 'info', '休学': 'warning',
  '紧急': 'danger', '高': 'warning', '普通': '', '低': 'info',
  '优秀': 'success', '良好': '', '合格': 'warning', '不合格': 'danger'
}
function tagType(prop, val) {
  if (!['status', 'priority', 'grade'].includes(prop)) return null
  if (val === '-' || val == null) return null
  return Object.prototype.hasOwnProperty.call(TAG_MAP, val) ? (TAG_MAP[val] || '') : null
}
function display(row, prop) {""")

patch("src/components/CrudPage.vue",
"""onMounted(load)
</script>""",
"""onMounted(load)
</script>
<style scoped>
.page-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid #eef2f7; }
.page-title { font-size: 17px; font-weight: 700; color: #22364f; padding-left: 10px; border-left: 4px solid #2f7de1; line-height: 1.1; }
.page-count { color: #a3b1c2; font-size: 12.5px; }
</style>""")

# ---------- index.html：favicon + 标题 ----------
patch("index.html",
'<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
'''<meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='22' fill='%232f7de1'/%3E%3Cpath d='M50 22 L82 50 H74 V78 H60 V62 H40 V78 H26 V50 H18 Z' fill='white'/%3E%3C/svg%3E" />''')

# ---------- Register 页背景与新主题统一 ----------
patch("src/views/Register.vue",
"background: linear-gradient(135deg, #1d4e89, #409eff 60%, #79bbff); padding: 24px 0; }",
"background: radial-gradient(900px 480px at 15% 10%, rgba(84,169,255,.5), transparent 60%), radial-gradient(800px 500px at 88% 90%, rgba(38,198,218,.35), transparent 60%), linear-gradient(135deg, #173a5e, #1d4e89 45%, #2f7de1); padding: 24px 0; }")
patch("src/views/Register.vue", ".login-card { width: 440px; padding: 10px; border-radius: 12px; }",
".login-card { width: 440px; padding: 14px; border-radius: 18px !important; }")
print("BEAUTIFY PART 2 DONE")
