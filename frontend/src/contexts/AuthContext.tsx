import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

interface User {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
}

interface AuthContextType {
  token: string | null;
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isAdmin: () => boolean;
  loadUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Simple JWT decoder (basic implementation)
const decodeJWT = (token: string): any => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<User | null>(null);

  const loadUser = async () => {
    if (!token) return;
    
    try {
      // Fetch user info from /me endpoint
      const response = await api.get('/auth/me');
      setUser(response.data);
      // Store is_admin in localStorage for quick access
      if (response.data.is_admin) {
        localStorage.setItem('is_admin', 'true');
      } else {
        localStorage.removeItem('is_admin');
      }
    } catch (err) {
      console.error('Failed to load user:', err);
      // If /me fails, try to decode from token as fallback
      const decoded = decodeJWT(token);
      if (decoded && decoded.sub) {
        const userInfo: User = {
          id: 0,
          username: decoded.sub,
          email: '',
          is_admin: decoded.is_admin || false,
        };
        setUser(userInfo);
        if (decoded.is_admin) {
          localStorage.setItem('is_admin', 'true');
        }
      }
    }
  };

  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      loadUser();
    } else {
      delete api.defaults.headers.common['Authorization'];
      setUser(null);
    }
  }, [token]);

  const login = async (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    const { access_token } = response.data;
    setToken(access_token);
    localStorage.setItem('token', access_token);
    
    // Load user info after login
    await loadUser();
  };

  const register = async (username: string, email: string, password: string) => {
    const response = await api.post('/auth/register', {
      username,
      email,
      password,
    });
    
    // Store user info from registration response
    if (response.data) {
      setUser(response.data);
    }
    
    // Auto-login after registration
    await login(username, password);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
  };

  const isAdmin = () => {
    // Check localStorage for admin status or decode from token
    // Since we can't easily decode is_admin from token without modifying backend,
    // we'll check user object or try a different approach
    return user?.is_admin || localStorage.getItem('is_admin') === 'true' || false;
  };

  return (
    <AuthContext.Provider value={{ token, user, login, register, logout, isAdmin, loadUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

