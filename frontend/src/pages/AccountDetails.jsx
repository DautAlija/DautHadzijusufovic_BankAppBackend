import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import api from '../api'

function AccountDetails() {
  const { accountId } = useParams()
  const [account, setAccount] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // useParams reads values from the current URL so this page can know which account ID is requested.
  // useEffect is used because the API call should happen after the component mounts and when the route param is available.
  useEffect(() => {
    const fetchAccount = async () => {
      try {
        setLoading(true)
        setError('')
        const response = await api.get('/api/accounts/' + accountId)
        setAccount(response.data)
      } catch (err) {
        setError('Account not found or could not be loaded.')
      } finally {
        setLoading(false)
      }
    }

    if (accountId) {
      fetchAccount()
    }
  }, [accountId])

  if (loading) {
    return <p style={{ textAlign: 'center', marginTop: '40px' }}>Loading account details...</p>
  }

  if (error || !account) {
    return <p style={{ textAlign: 'center', marginTop: '40px', color: 'crimson' }}>{error || 'Account not found.'}</p>
  }

  return (
    <div style={{ maxWidth: '500px', margin: '40px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Account Details</h1>

      <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '16px', marginBottom: '20px' }}>
        <p><strong>Account ID:</strong> {account.account_id}</p>
        <p><strong>User ID:</strong> {account.user_id}</p>
        <p><strong>Balance:</strong> ${Number(account.balance).toFixed(2)}</p>
        <p><strong>Account Type:</strong> {account.account_type}</p>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', justifyContent: 'center' }}>
        <Link to={`/account/${accountId}/deposit`}>
          <button type="button">Deposit</button>
        </Link>
        <Link to={`/account/${accountId}/withdraw`}>
          <button type="button">Withdraw</button>
        </Link>
        <Link to={`/account/${accountId}/transactions`}>
          <button type="button">View Transactions</button>
        </Link>
      </div>
    </div>
  )
}

export default AccountDetails
