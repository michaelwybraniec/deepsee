import { useState, useMemo, createContext, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../services/api';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [user, setUser] = useState(() => {
    // Load user from localStorage on mount
    const storedUser = localStorage.getItem('user');
    return storedUser ? JSON.parse(storedUser) : null;
  });
  const navigate = useNavigate();

  // Derive isAuthenticated from token instead of storing as separate state
  const isAuthenticated = useMemo(() => !!token, [token]);

  const login = async (username, password) => {
    try {
      const response = await apiClient.post('/api/auth/login', {
        username,
        password,
      });
      
      const { token: newToken, user: userData } = response.data;
      
      // Store token and user
      localStorage.setItem('token', newToken);
      localStorage.setItem('user', JSON.stringify(userData));
      setToken(newToken);
      setUser(userData);
      
      return { success: true, user: userData };
    } catch (error) {
      let errorMessage = 'Login failed';
      
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        // Handle both string and object error formats
        if (typeof detail === 'string') {
          errorMessage = detail;
        } else if (detail.error?.message) {
          errorMessage = detail.error.message;
        } else if (detail.message) {
          errorMessage = detail.message;
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      return { success: false, error: errorMessage };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    navigate('/login');
  };

  const changePassword = async (currentPassword, newPassword) => {
    try {
      await apiClient.post('/api/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      });
      
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Password change failed';
      return { success: false, error: errorMessage };
    }
  };

  const value = {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    changePassword,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Hook for using auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthProvider;
