import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

// baseURL keeps all requests pointed at the backend root, so we can use paths like /api/accounts without repeating the host.
// Route parameters like :accountId let the app target the correct account in a URL such as /account/42.

export default api
