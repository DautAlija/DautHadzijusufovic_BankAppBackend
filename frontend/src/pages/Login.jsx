import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import api from '../api'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')

    try {
      const response = await api.post('/api/login', { email, password })
      localStorage.setItem('token', response.data.access_token)
      navigate('/')
    } catch (err) {
      setError('Login failed. Please check your email and password.')
    }
  }

  return (
    <div style={{ maxWidth: '420px', margin: '40px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Login</h1>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <label>
          <span style={{ display: 'block', marginBottom: '6px' }}>Email</span>
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box' }}
          />
        </label>

        <label>
          <span style={{ display: 'block', marginBottom: '6px' }}>Password</span>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box' }}
          />
        </label>

        <button type="submit" style={{ padding: '10px 16px', cursor: 'pointer' }}>
          Login
        </button>
      </form>

      <p style={{ textAlign: 'center', marginTop: '16px' }}>
        Need an account?{' '}
        <Link to="/register">Register</Link>
      </p>

      {error && <p style={{ marginTop: '16px', color: 'crimson', textAlign: 'center' }}>{error}</p>}
    </div>
  )
}

export default Login
