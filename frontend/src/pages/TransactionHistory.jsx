import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import api from '../api'

function TransactionHistory() {
  const { accountId } = useParams()
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await api.get('/api/accounts/' + accountId + '/transactions')
        setTransactions(Array.isArray(response.data) ? response.data : [])
      } finally {
        setLoading(false)
      }
    }

    if (accountId) {
      fetchTransactions()
    }
  }, [accountId])

  if (loading) {
    return <p style={{ textAlign: 'center', marginTop: '40px' }}>Loading transactions...</p>
  }

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Transaction History</h1>

      {transactions.length === 0 ? (
        <p style={{ textAlign: 'center' }}>No transactions yet</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid #ddd', padding: '10px', textAlign: 'left' }}>Transaction ID</th>
              <th style={{ border: '1px solid #ddd', padding: '10px', textAlign: 'left' }}>Type</th>
              <th style={{ border: '1px solid #ddd', padding: '10px', textAlign: 'left' }}>Amount</th>
              <th style={{ border: '1px solid #ddd', padding: '10px', textAlign: 'left' }}>Date</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.txn_id ?? `${transaction.txn_type}-${transaction.created_at}`}>
                <td style={{ border: '1px solid #ddd', padding: '10px' }}>{transaction.txn_id}</td>
                <td style={{ border: '1px solid #ddd', padding: '10px' }}>{transaction.txn_type}</td>
                <td style={{ border: '1px solid #ddd', padding: '10px' }}>${Number(transaction.amount).toFixed(2)}</td>
                <td style={{ border: '1px solid #ddd', padding: '10px' }}>{transaction.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div style={{ textAlign: 'center' }}>
        <Link to={`/account/${accountId}`}>
          <button type="button">Back to Account</button>
        </Link>
      </div>
    </div>
  )
}

export default TransactionHistory
