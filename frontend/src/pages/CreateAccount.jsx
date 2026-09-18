import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import api from '../api'

function CreateAccount() {
  const [user, setUser] = useState(null)
  const [userId, setUserId] = useState('')
  const [accountType, setAccountType] = useState('SAVINGS')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const fetchCurrentUser = async () => {
      try {
        const response = await api.get('/api/me')
        setUser(response.data)
        setUserId(response.data.user_id)
      } catch (err) {
        setError('Unable to load your profile. Please log in again.')
      }
    }

    fetchCurrentUser()
  }, [])

  // useNavigate lets us move to a different page after an action succeeds.
  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')

    try {
      const response = await api.post('/api/accounts', {
        userId: Number(userId),
        accountType,
      })

      const accountId = response.data.account_id ?? response.data.id

      if (accountId === undefined || accountId === null) {
        throw new Error('No account ID returned')
      }

      navigate(`/account/${accountId}`)
    } catch (err) {
      setError('Failed to create account. Please try again.')
    }
  }

  return (
    <div style={{ maxWidth: '420px', margin: '40px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ marginBottom: '20px', textAlign: 'center' }}>Create Account</h1>

      {user && (
        <p style={{ textAlign: 'center', marginBottom: '16px' }}>
          Creating account for: {user.name}
        </p>
      )}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <label>
          <span style={{ display: 'block', marginBottom: '6px' }}>User ID</span>
          <div
            style={{
              width: '100%',
              padding: '10px',
              boxSizing: 'border-box',
              border: '1px solid #ddd',
              borderRadius: '4px',
              background: '#f7f7f7',
            }}
          >
            {userId || 'Loading...'}
          </div>
        </label>

        <label>
          <span style={{ display: 'block', marginBottom: '6px' }}>Account Type</span>
          <select
            value={accountType}
            onChange={(event) => setAccountType(event.target.value)}
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box' }}
          >
            <option value="SAVINGS">SAVINGS</option>
            <option value="CHECKING">CHECKING</option>
          </select>
        </label>

        <button type="submit" style={{ padding: '10px 16px', cursor: 'pointer' }}>
          Create Account
        </button>
      </form>

      {error && <p style={{ marginTop: '16px', color: 'crimson', textAlign: 'center' }}>{error}</p>}
    </div>
  )
}

export default CreateAccount
