import axios from 'axios'
import { ElMessage } from 'element-plus'
const request = axios.create({ baseURL: '/api', timeout: 15000 })
request.interceptors.request.use(cfg => {
  const token = localStorage.getItem('dorm_token')
  if (token) cfg.headers.Authorization = 'Bearer ' + token
  return cfg
})
request.interceptors.response.use(
  res => {
    const data = res.data
    if (data && typeof data.code === 'number' && data.code !== 200) {
      ElMessage.error(data.msg || '请求失败')
      return Promise.reject(new Error(data.msg || '请求失败'))
    }
    return data
  },
  err => {
    if (err.response && err.response.status === 403) ElMessage.error('无权访问')
    else if (err.response && err.response.status === 401) { localStorage.removeItem('dorm_token'); location.hash = '#/login' }
    else ElMessage.error(err.message || '网络错误')
    return Promise.reject(err)
  }
)
export default request
