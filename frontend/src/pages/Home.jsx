import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import api from '../api'

function Home() {
  const [accountId, setAccountId] = useState('')
  const [accounts, setAccounts] = useState([])
  const [role, setRole] = useState(null)
  const navigate = useNavigate()
  const isLoggedIn = !!localStorage.getItem('token')

  useEffect(() => {
    if (!isLoggedIn) return

    const fetchAccounts = async () => {
      try {
        const response = await api.get('/api/my-accounts')
        setAccounts(Array.isArray(response.data) ? response.data : [])
      } catch (err) {
        setAccounts([])
      }
    }

    const fetchMe = async () => {
      try {
        const response = await api.get('/api/me')
        setRole(response.data?.role ?? null)
      } catch (err) {
        setRole(null)
      }
    }

    fetchAccounts()
    fetchMe()
  }, [isLoggedIn])

  const handleViewAccount = () => {
    if (!accountId.trim()) return
    navigate(`/account/${accountId}`)
  }

  return (
    <div style={{ maxWidth: '500px', margin: '40px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '24px' }}>Simple Bank App</h1>

      {!isLoggedIn && (
        <p style={{ textAlign: 'center', marginBottom: '20px' }}>Please log in to view your accounts</p>
      )}

      {isLoggedIn && (
        <div style={{ marginBottom: '20px' }}>
          {accounts.length === 0 ? (
            <p style={{ textAlign: 'center' }}>No accounts yet</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
              {accounts.map((account) => (
                <li key={account.account_id} style={{ marginBottom: '10px', textAlign: 'center' }}>
                  <Link to={`/account/${account.account_id}`}>
                    {account.account_id} - {account.account_type}
                  </Link>
                </li>
              ))}
            </ul>
          )}

          <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
            <Link to="/create-account">
              <button type="button" style={{ padding: '10px 18px', cursor: 'pointer' }}>
                {accounts.length > 0 ? 'Add Another Account' : 'Create Account'}
              </button>
            </Link>
          </div>
        </div>
      )}

      {role === 'admin' && (
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <input
            type="text"
            value={accountId}
            onChange={(event) => setAccountId(event.target.value)}
            placeholder="Account ID"
            style={{ padding: '10px', flex: 1, minWidth: '120px' }}
          />
          <button type="button" onClick={handleViewAccount} style={{ padding: '10px 16px', cursor: 'pointer' }}>
            View Account
          </button>
        </div>
      )}
    </div>
  )
}

export default Home
