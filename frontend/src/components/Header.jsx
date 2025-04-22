import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between h-16">
          {/* Logo / Titel */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-xl font-bold text-gray-800 hover:text-blue-600">
              🖥️ PC Webshop
            </Link>
          </div>

          {/* Navigation Links */}
          <ul className="flex space-x-6 text-sm font-medium">
            <li>
              <Link to="/" className="text-gray-700 hover:text-blue-600 transition-colors">
                Home
              </Link>
            </li>
            <li>
              <Link to="/components" className="text-gray-700 hover:text-blue-600 transition-colors">
                Komponenten
              </Link>
            </li>
            <li>
              <Link to="/configurator" className="text-gray-700 hover:text-blue-600 transition-colors">
                Konfigurator
              </Link>
            </li>
            <li>
              <Link to="/cart" className="text-gray-700 hover:text-blue-600 transition-colors">
                Warenkorb
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;