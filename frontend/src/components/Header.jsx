import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { isLoggedIn, logout } from '../utils/auth';
import { useEffect, useState } from 'react';
import { useCart } from '../context/CartContext';

function Header() {
  const navigate = useNavigate();
  const location = useLocation(); // ✅ aktueller Pfad
  const [username, setUsername] = useState('');
  const { cartItems } = useCart();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  useEffect(() => {
    if (!isLoggedIn()) return;

    const token = localStorage.getItem('accessToken');
    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.user_id;

    fetch(`http://127.0.0.1:8000/users/${userId}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setUsername(data.username))
      .catch((err) => console.error('Failed to fetch user:', err));
  }, []);

  const navLinkClass = (path) =>
    `group relative transition-all duration-300 ${
      location.pathname === path
        ? 'text-cyan-400'
        : 'text-white hover:text-cyan-400'
    }`;

  return (
    <motion.header
      initial={{ opacity: 0, y: -15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="bg-gradient-to-r from-[#0f172a] via-[#1e293b] to-[#0f172a] shadow-md sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between h-20">
          {/* Logo / Title */}
          <div className="flex-shrink-0">
            <Link
              to="/"
              className="text-3xl font-bold text-white hover:text-cyan-400 transition-colors drop-shadow-[0_1px_1px_rgba(0,0,0,0.5)]"
            >
              🖥️ Nico's PC Webshop
            </Link>
          </div>

          {/* Navigation + Username */}
          <div className="flex items-center gap-12 min-w-0">
            <ul className="flex space-x-10 text-lg font-medium">
              <li>
                <Link to="/components" className={navLinkClass('/components')}>
                  <span className="inline-block group-hover:-translate-y-0.5 transition-transform duration-300">
                    Products
                  </span>
                  <span className="absolute left-0 -bottom-1 w-0 h-0.5 bg-cyan-400 transition-all duration-300 group-hover:w-full"></span>
                </Link>
              </li>
              <li>
                <Link to="/configurator" className={navLinkClass('/configurator')}>
                  <span className="inline-block group-hover:-translate-y-0.5 transition-transform duration-300">
                    Configurator
                  </span>
                  <span className="absolute left-0 -bottom-1 w-0 h-0.5 bg-cyan-400 transition-all duration-300 group-hover:w-full"></span>
                </Link>
              </li>
              <li>
                <Link to="/cart" className={navLinkClass('/cart')}>
                  <span className="inline-block group-hover:-translate-y-0.5 transition-transform duration-300">
                    Cart {cartItems.length > 0 && `(${cartItems.length})`}
                  </span>
                  <span className="absolute left-0 -bottom-1 w-0 h-0.5 bg-cyan-400 transition-all duration-300 group-hover:w-full"></span>
                </Link>
              </li>

              {/* Login / Logout */}
              <li>
                {isLoggedIn() ? (
                  <button
                    onClick={handleLogout}
                    className="group relative text-white hover:text-cyan-400 transition-all duration-300"
                  >
                    <span className="inline-block group-hover:-translate-y-0.5 transition-transform duration-300">
                      Logout
                    </span>
                    <span className="absolute left-0 -bottom-1 w-0 h-0.5 bg-cyan-400 transition-all duration-300 group-hover:w-full"></span>
                  </button>
                ) : (
                  <Link
                    to="/login"
                    className={navLinkClass('/login')}
                  >
                    <span className="inline-block group-hover:-translate-y-0.5 transition-transform duration-300">
                      Login
                    </span>
                    <span className="absolute left-0 -bottom-1 w-0 h-0.5 bg-cyan-400 transition-all duration-300 group-hover:w-full"></span>
                  </Link>
                )}
              </li>
            </ul>

            {/* Username */}
            {isLoggedIn() && username && (
              <div className="text-right text-white text-sm font-medium max-w-xs">
                <span className="text-gray-400 mr-1">Logged in as:</span>
                <span className="text-cyan-400 font-semibold">{username}</span>
              </div>
            )}
          </div>
        </nav>
      </div>
    </motion.header>
  );
}

export default Header;