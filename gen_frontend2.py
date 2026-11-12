#!/usr/bin/env python3
import os, textwrap
ROOT = os.path.expanduser("~/workspace/dorm-system/frontend")
def w(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("wrote", rel)

w("src/components/CrudPage.vue", r'''
<template>
  <div>
    <el-card shadow="never">
      <div style="display:flex;gap:12px;margin-bottom:16px;align-items:center">
        <el-input v-model="keyword" :placeholder="config.searchPlaceholder || '搜索'" style="width:280px" clearable @keyup.enter="load" @clear="load" />
        <el-button type="primary" @click="load">搜索</el-button>
        <el-button v-if="config.assignApi" type="success" @click="openAssign">入住分配</el-button>
        <el-button type="primary" plain @click="openCreate" style="margin-left:auto">+ 新增{{ config.title.replace('管理','').replace('审批','') }}</el-button>
      </div>
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column type="index" label="#" width="55" />
        <el-table-column v-for="c in config.columns" :key="c.prop" :label="c.label" :width="c.width" show-overflow-tooltip>
          <template #default="{ row }">{{ display(row, c.prop) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="230" fixed="right">
          <template #default="{ row }">
            <el-button v-for="a in (config.rowActions || []).filter(x => !x.show || x.show(row))" :key="a.label" size="small" :type="a.type || 'primary'" @click="runAction(a, row)">{{ a.label }}</el-button>
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination style="margin-top:16px;justify-content:flex-end;display:flex" background layout="total, prev, pager, next, sizes"
        :total="total" v-model:current-page="page" v-model:page-size="size" :page-sizes="[10,20,50]" @current-change="load" @size-change="load" />
    </el-card>

    <el-dialog v-model="dialog" :title="(form.id ? '编辑' : '新增') + ' - ' + config.title" width="620px">
      <el-form :model="form" label-width="100px">
        <el-form-item v-for="f in config.fields" :key="f.prop" :label="f.label" :required="f.required">
          <el-input v-if="!f.type || f.type === 'text'" v-model="form[f.prop]" />
          <el-input-number v-else-if="f.type === 'number'" v-model="form[f.prop]" style="width:100%" />
          <el-select v-else-if="f.type === 'select'" v-model="form[f.prop]" style="width:100%">
            <el-option v-for="o in f.options" :key="o" :label="o" :value="o" />
          </el-select>
          <el-select v-else-if="f.type === 'fk'" v-model="form[f.prop + 'Id']" style="width:100%" clearable filterable>
            <el-option v-for="o in fkOptions[f.prop] || []" :key="o.id" :label="f.optionLabel(o)" :value="o.id" />
          </el-select>
          <el-date-picker v-else-if="f.type === 'date'" v-model="form[f.prop]" type="date" value-format="YYYY-MM-DD" style="width:100%" />
          <el-date-picker v-else-if="f.type === 'datetime'" v-model="form[f.prop]" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width:100%" />
          <el-switch v-else-if="f.type === 'switch'" v-model="form[f.prop]" />
          <el-input v-else-if="f.type === 'textarea'" v-model="form[f.prop]" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-if="config.assignApi" v-model="assignDialog" title="入住分配（选择学生与空闲床位）" width="520px">
      <el-form label-width="90px">
        <el-form-item label="学生">
          <el-select v-model="assign.studentId" style="width:100%" filterable>
            <el-option v-for="s in assignStudents" :key="s.id" :label="s.name + '（' + s.studentNo + '）'" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="空闲床位">
          <el-select v-model="assign.bedId" style="width:100%" filterable>
            <el-option v-for="b in assignBeds" :key="b.id" :label="(b.room && b.room.building ? b.room.building.name + ' ' : '') + (b.room ? b.room.roomNo : '') + ' ' + b.bedNo" :value="b.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注"><el-input v-model="assign.remark" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="assignDialog = false">取消</el-button>
        <el-button type="primary" @click="doAssign">确认分配</el-button>
      </template>
    </el-dialog>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../utils/request'
const props = defineProps({ config: { type: Object, required: true } })
const config = props.config
const rows = ref([]), total = ref(0), page = ref(1), size = ref(10)
const keyword = ref(''), loading = ref(false)
const dialog = ref(false), form = ref({})
const fkOptions = ref({})
const assignDialog = ref(false), assign = ref({ studentId: null, bedId: null, remark: '' })
const assignStudents = ref([]), assignBeds = ref([])

function display(row, prop) {
  const v = prop.split('.').reduce((o, k) => (o == null ? o : o[k]), row)
  if (typeof v === 'boolean') return v ? '是' : '否'
  return v == null || v === '' ? '-' : v
}
async function loadFk() {
  for (const f of config.fields) {
    if (f.type === 'fk' && !fkOptions.value[f.prop]) {
      const res = await request.get(f.endpoint)
      fkOptions.value[f.prop] = res.data || []
    }
  }
}
async function load() {
  loading.value = true
  try {
    const params = { page: page.value, size: size.value }
    if (keyword.value && config.searchKey) params[config.searchKey] = keyword.value
    const res = await request.get(config.endpoint, { params })
    rows.value = res.data.records; total.value = res.data.total
  } finally { loading.value = false }
}
function blankForm() {
  const o = {}
  for (const f of config.fields) { o[f.prop] = f.type === 'switch' ? false : (f.type === 'fk' ? undefined : ''); if (f.type === 'fk') o[f.prop + 'Id'] = null }
  return o
}
async function openCreate() { form.value = blankForm(); await loadFk(); dialog.value = true }
async function openEdit(row) {
  await loadFk()
  const o = blankForm(); o.id = row.id
  for (const f of config.fields) {
    if (f.type === 'fk') { o[f.prop + 'Id'] = row[f.prop] ? row[f.prop].id : null }
    else o[f.prop] = row[f.prop]
  }
  form.value = o; dialog.value = true
}
function buildPayload() {
  const o = {}
  if (form.value.id) o.id = form.value.id
  for (const f of config.fields) {
    if (f.type === 'fk') { o[f.prop] = form.value[f.prop + 'Id'] ? { id: form.value[f.prop + 'Id'] } : null }
    else if (form.value[f.prop] !== '' && form.value[f.prop] !== undefined) o[f.prop] = form.value[f.prop]
  }
  return o
}
async function save() {
  const payload = buildPayload()
  if (form.value.id) await request.put(config.endpoint + '/' + form.value.id, payload)
  else await request.post(config.endpoint, payload)
  ElMessage.success('保存成功'); dialog.value = false; load()
}
async function remove(row) {
  await ElMessageBox.confirm('确认删除该记录？', '提示', { type: 'warning' })
  await request.delete(config.endpoint + '/' + row.id)
  ElMessage.success('删除成功'); load()
}
async function runAction(a, row) {
  if (a.confirm) await ElMessageBox.confirm(a.confirm, '提示', { type: 'warning' })
  await request[a.method || 'post'](a.url(row))
  ElMessage.success('操作成功'); load()
}
async function openAssign() {
  const s = await request.get('/students/all'); assignStudents.value = s.data || []
  const b = await request.get('/beds/all'); assignBeds.value = (b.data || []).filter(x => x.status === '空闲')
  assignDialog.value = true
}
async function doAssign() {
  await request.post('/checkins/assign', assign.value)
  ElMessage.success('分配成功'); assignDialog.value = false; load()
}
onMounted(load)
</script>
''')

w("src/layout/MainLayout.vue", r'''
<template>
  <el-container style="height:100vh">
    <el-aside width="220px" style="background:#304156;color:#fff">
      <div style="padding:18px 16px;font-size:17px;font-weight:bold;border-bottom:1px solid #3d5269">
        <el-icon style="vertical-align:-2px"><House /></el-icon> 宿舍管理系统
      </div>
      <el-menu :default-active="$route.path" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409eff" style="border:0">
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
    </el-aside>
    <el-container>
      <el-header style="background:#fff;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 4px rgba(0,0,0,.08)">
        <span style="font-size:16px;font-weight:600">{{ $route.meta.title || '宿舍管理系统' }}</span>
        <el-dropdown @command="cmd">
          <span style="cursor:pointer">{{ auth.user ? auth.user.realName || auth.user.username : '' }}（{{ roleName }}）<el-icon><ArrowDown /></el-icon></span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main><router-view /></el-main>
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
function cmd(c) {
  if (c === 'logout') { auth.logout(); router.push('/login') }
  if (c === 'profile') router.push('/profile')
}
</script>
''')
print("FRONT PART B DONE")
