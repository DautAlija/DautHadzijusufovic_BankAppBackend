import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import api from '../api'

function Withdraw() {
  const { accountId } = useParams()
  const [amount, setAmount] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')

    try {
      await api.post('/api/accounts/' + accountId + '/withdraw', {
        amount: Number(amount),
      })
      navigate(`/account/${accountId}`)
    } catch (err) {
      const detail = err.response?.data?.detail
      setError(detail || 'Withdrawal failed. Please check the amount and try again.')
    }
  }

  return (
    <div style={{ maxWidth: '420px', margin: '40px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Withdraw</h1>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <label>
          <span style={{ display: 'block', marginBottom: '6px' }}>Amount</span>
          <input
            type="number"
            min="0.01"
            step="0.01"
            value={amount}
            onChange={(event) => setAmount(event.target.value)}
            required
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box' }}
          />
        </label>

        <button type="submit" style={{ padding: '10px 16px', cursor: 'pointer' }}>
          Submit Withdrawal
        </button>
      </form>

      {error && <p style={{ marginTop: '16px', color: 'crimson', textAlign: 'center' }}>{error}</p>}
    </div>
  )
}

export default Withdraw
