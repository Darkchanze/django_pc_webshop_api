import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/users/', formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setMessage('User registered successfully!');
      console.log(response.data);
    } catch (error) {
      console.error(error);
      setMessage('Registration failed.');
    }
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-white flex flex-col justify-center items-center px-4">
      <form
        onSubmit={handleSubmit}
        className="bg-[#1e293b] p-8 rounded-xl shadow-xl w-full max-w-md space-y-6"
      >
        <h2 className="text-3xl font-bold text-center text-white">Register</h2>

        {message && (
          <p className={`text-center ${message.includes('successfully') ? 'text-green-400' : 'text-red-400'}`}>
            {message}
          </p>
        )}

        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          className="w-full p-3 rounded bg-[#0f172a] border border-gray-700 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          className="w-full p-3 rounded bg-[#0f172a] border border-gray-700 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          className="w-full p-3 rounded bg-[#0f172a] border border-gray-700 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          required
        />
        <button
          type="submit"
          className="w-full py-3 bg-cyan-500 hover:bg-cyan-400 text-black font-semibold rounded transition"
        >
          Register
        </button>

        {/* Link zurück zu Login */}
        <p className="text-center text-gray-400 mt-4">
          Already have an account?{' '}
          <Link to="/login" className="text-cyan-400 hover:underline">
            Login here
          </Link>
        </p>
      </form>
    </div>
  );
};

export default Register;