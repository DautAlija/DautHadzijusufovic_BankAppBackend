import { Link } from 'react-router-dom'

function Nav() {
  const isLoggedIn = !!localStorage.getItem('token')

  const handleLogout = () => {
    localStorage.removeItem('token')
    window.location.reload()
  }

  return (
    <nav
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderBottom: '1px solid #ddd',
        padding: '8px 16px',
        background: '#fff',
      }}
    >
      <Link to="/" style={{ textDecoration: 'none', color: '#333', fontWeight: 'bold' }}>
        Home
      </Link>

      {isLoggedIn ? (
        <button type="button" onClick={handleLogout} style={{ padding: '6px 10px', cursor: 'pointer' }}>
          Logout
        </button>
      ) : (
        <div style={{ display: 'flex', gap: '12px' }}>
          <Link to="/login" style={{ textDecoration: 'none', color: '#333' }}>
            Login
          </Link>
          <Link to="/register" style={{ textDecoration: 'none', color: '#333' }}>
            Register
          </Link>
        </div>
      )}
    </nav>
  )
}

export default Nav
