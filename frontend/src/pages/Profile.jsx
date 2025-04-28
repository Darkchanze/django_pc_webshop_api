import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    password: '********',
  });
  const [editField, setEditField] = useState('');
  const accessToken = localStorage.getItem('accessToken');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        const payload = JSON.parse(atob(token.split('.')[1]));
        const userId = payload.user_id;

        const userResponse = await axios.get(`http://127.0.0.1:8000/users/${userId}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        setUserData({
          username: userResponse.data.username || '',
          email: userResponse.data.email || '',
          password: '********', // Passwort immer Sternchen
        });

      } catch (error) {
        console.error('Failed to load profile:', error);
      }
    };
    fetchProfile();
  }, [accessToken]);

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleSave = async (field) => {
    try {
      const updatePayload = {};
      if (field === 'password' && userData.password === '********') {
        alert('Please enter a new password to update.');
        return;
      }
      updatePayload[field] = userData[field];

      const token = localStorage.getItem('accessToken');
      const payload = JSON.parse(atob(token.split('.')[1]));
      const userId = payload.user_id;

      await axios.patch(`http://127.0.0.1:8000/users/${userId}/`, updatePayload, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      setEditField('');
    } catch (error) {
      console.error('Failed to save changes:', error);
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      try {
        const token = localStorage.getItem('accessToken');
        const payload = JSON.parse(atob(token.split('.')[1]));
        const userId = payload.user_id;

        await axios.delete(`http://127.0.0.1:8000/users/${userId}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        navigate('/login');
      } catch (error) {
        console.error('Failed to delete account:', error);
      }
    }
  };

  const renderField = (label, fieldName, type = 'text') => (
    <div className="flex flex-col mb-6">
      <label className="text-cyan-400 mb-2">{label}</label>
      {editField === fieldName ? (
        <div className="flex items-center gap-2">
          <input
            type={type}
            name={fieldName}
            value={userData[fieldName] || ''}
            onChange={handleChange}
            className="w-full p-3 rounded bg-[#0f172a] border border-gray-700 focus:ring-2 focus:ring-cyan-500"
          />
          <button
            type="button"
            onClick={() => handleSave(fieldName)}
            className="py-2 px-4 bg-green-500 hover:bg-green-400 rounded text-black font-bold"
          >
            Save
          </button>
        </div>
      ) : (
        <div className="flex items-center gap-2">
          <div className="flex-1 p-3 rounded bg-[#0f172a] border border-gray-700">
            {fieldName === 'password' ? '********' : (userData[fieldName] || 'Not set')}
          </div>
          <button
            type="button"
            onClick={() => setEditField(fieldName)}
            className="py-2 px-4 bg-cyan-500 hover:bg-cyan-400 rounded text-black font-bold"
          >
            Edit
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-[#0f172a] text-white flex flex-col justify-center items-center px-4 py-10">
      <div className="bg-[#1e293b] p-8 rounded-xl shadow-xl w-full max-w-2xl space-y-10">
        <h2 className="text-3xl font-bold text-center">User Profile</h2>

        {/* Profile Details */}
        <div>
          <h3 className="text-xl font-semibold mb-6 text-cyan-400">Profile Details</h3>
          {renderField('Username', 'username')}
          {renderField('Email', 'email')}
          {renderField('Password', 'password', 'password')}
        </div>

        {/* My Orders */}
        <div>
          <h3 className="text-xl font-semibold mb-6 text-cyan-400">My Orders</h3>
          <p className="text-gray-400">No orders yet. Start shopping now!</p>
        </div>

        {/* Delete Account Button */}
        <div className="pt-6">
          <button
            type="button"
            onClick={handleDeleteAccount}
            className="w-full py-3 bg-red-500 hover:bg-red-400 text-white font-semibold rounded transition"
          >
            Delete Account
          </button>
        </div>
      </div>
    </div>
  );
};

export default Profile;