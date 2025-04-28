import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="bg-[#1e293b] text-gray-400 text-sm py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-6">

        {/* Navigation Links */}
        <div className="flex gap-6">
          <Link to="/" className="hover:text-cyan-400 transition-colors">Home</Link>
          <Link to="/components" className="hover:text-cyan-400 transition-colors">Products</Link>
          <Link to="/cart" className="hover:text-cyan-400 transition-colors">Cart</Link>
        </div>

        {/* Copyright */}
        <div className="text-center md:text-right">
          © 2025 Nico's PC Webshop – All rights reserved.
        </div>
      </div>
    </footer>
  );
}

export default Footer;