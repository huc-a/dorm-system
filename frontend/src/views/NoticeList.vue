<template>
  <el-card shadow="never">
    <el-timeline>
      <el-timeline-item v-for="n in list" :key="n.id" :timestamp="(n.publishTime || '').replace('T', ' ').slice(0, 16)" placement="top">
        <el-tag size="small">{{ n.type }}</el-tag>
        <el-tag v-if="n.top" type="danger" size="small" style="margin-left:6px">置顶</el-tag>
        <h4 style="margin:8px 0 4px">{{ n.title }}</h4>
        <div style="color:#606266;white-space:pre-wrap">{{ n.content }}</div>
        <div style="color:#909399;font-size:12px;margin-top:4px">发布：{{ n.publisher }}</div>
      </el-timeline-item>
    </el-timeline>
    <el-empty v-if="!list.length" description="暂无公告" />
  </el-card>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import request from '../utils/request'
const list = ref([])
onMounted(async () => { const res = await request.get('/notices/all'); list.value = res.data || [] })
</script>
