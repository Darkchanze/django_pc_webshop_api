import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

function NotFound() {
  return (
    <div className="min-h-screen bg-[#0f172a] text-white flex flex-col items-center justify-center px-6 text-center">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="space-y-6"
      >
        <div className="text-6xl">🚫</div>
        <h1 className="text-4xl font-bold text-red-500">404 – Page not found</h1>
        <p className="text-gray-400 max-w-md">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link
          to="/"
          className="inline-block mt-4 bg-cyan-500 hover:bg-cyan-400 text-black font-semibold px-6 py-3 rounded-lg shadow transition"
        >
          Back to Home
        </Link>
      </motion.div>
    </div>
  );
}

export default NotFound;