<template>
  <div>
    <el-card shadow="never">
      <div class="page-head">
        <div class="page-title">{{ config.title }}</div>
        <div class="page-count">共 {{ total }} 条记录</div>
      </div>
      <div style="display:flex;gap:12px;margin-bottom:16px;align-items:center">
        <el-input v-model="keyword" :placeholder="config.searchPlaceholder || '搜索'" style="width:280px" clearable @keyup.enter="load" @clear="load" />
        <el-button type="primary" @click="load">搜索</el-button>
        <el-button v-if="config.assignApi" type="success" @click="openAssign">入住分配</el-button>
        <el-button type="primary" plain @click="openCreate" style="margin-left:auto">+ 新增{{ config.title.replace('管理','').replace('审批','') }}</el-button>
      </div>
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column type="index" label="#" width="55" />
        <el-table-column v-for="c in config.columns" :key="c.prop" :label="c.label" :width="c.width" show-overflow-tooltip>
          <template #default="{ row }">
            <el-tag v-if="tagType(c.prop, display(row, c.prop)) !== null" :type="tagType(c.prop, display(row, c.prop)) || 'primary'" effect="light" size="small">{{ display(row, c.prop) }}</el-tag>
            <span v-else>{{ display(row, c.prop) }}</span>
          </template>
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

const TAG_MAP = {
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
<style scoped>
.page-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid #eef2f7; }
.page-title { font-size: 17px; font-weight: 700; color: #22364f; padding-left: 10px; border-left: 4px solid #2f7de1; line-height: 1.1; }
.page-count { color: #a3b1c2; font-size: 12.5px; }
</style>
