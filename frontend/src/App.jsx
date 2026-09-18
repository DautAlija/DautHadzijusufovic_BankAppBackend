import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import CreateAccount from './pages/CreateAccount'
import AccountDetails from './pages/AccountDetails'
import Deposit from './pages/Deposit'
import Withdraw from './pages/Withdraw'
import TransactionHistory from './pages/TransactionHistory'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create-account" element={<CreateAccount />} />
        <Route path="/account/:accountId" element={<AccountDetails />} />
        <Route path="/account/:accountId/deposit" element={<Deposit />} />
        <Route path="/account/:accountId/withdraw" element={<Withdraw />} />
        <Route path="/account/:accountId/transactions" element={<TransactionHistory />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
