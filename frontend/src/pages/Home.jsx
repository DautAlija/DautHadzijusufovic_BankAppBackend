import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

function Home() {
  const [accountId, setAccountId] = useState('')
  const navigate = useNavigate()

  const handleViewAccount = () => {
    if (!accountId.trim()) return
    navigate(`/account/${accountId}`)
  }

  return (
    <div style={{ maxWidth: '500px', margin: '40px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '24px' }}>Simple Bank App</h1>

      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
        <Link to="/create-account">
          <button type="button" style={{ padding: '10px 18px', cursor: 'pointer' }}>
            Create Account
          </button>
        </Link>
      </div>

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
    </div>
  )
}

export default Home
