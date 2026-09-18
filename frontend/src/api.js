import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

// An interceptor runs automatically before each request, so we can attach common auth data in one place.
// This keeps every existing api.get()/api.post() call authenticated without editing each page individually.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

// baseURL keeps all requests pointed at the backend root, so we can use paths like /api/accounts without repeating the host.
// Route parameters like :accountId let the app target the correct account in a URL such as /account/42.

export default api
