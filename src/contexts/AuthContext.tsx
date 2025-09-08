import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiService, User } from '@/services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  googleLogin: (credential: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Load user from localStorage on app start
  useEffect(() => {
    // Clear any existing test data on app start
    localStorage.clear();
    
    const savedUser = localStorage.getItem('nova_user');
    const savedToken = localStorage.getItem('nova_token');
    
    if (savedUser && savedToken) {
      try {
        setUser(JSON.parse(savedUser));
        setToken(savedToken);
      } catch (error) {
        console.error('Failed to parse saved user data:', error);
        localStorage.removeItem('nova_user');
        localStorage.removeItem('nova_token');
      }
    }
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const result = await apiService.login(email, password);
      
      setUser(result.user);
      setToken(result.token);
      
      // Save to localStorage
      localStorage.setItem('nova_user', JSON.stringify(result.user));
      localStorage.setItem('nova_token', result.token);
      
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (name: string, email: string, password: string) => {
    setIsLoading(true);
    try {
      const result = await apiService.signup(name, email, password);
      
      setUser(result.user);
      setToken(result.token);
      
      // Save to localStorage
      localStorage.setItem('nova_user', JSON.stringify(result.user));
      localStorage.setItem('nova_token', result.token);
      
    } catch (error) {
      console.error('Signup failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const googleLogin = async (credential: string) => {
    setIsLoading(true);
    try {
      const result = await apiService.googleAuth(credential);
      
      setUser(result.user);
      setToken(result.token);
      
      // Save to localStorage
      localStorage.setItem('nova_user', JSON.stringify(result.user));
      localStorage.setItem('nova_token', result.token);
      
    } catch (error) {
      console.error('Google login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    
    // Clear all stored data including any test data
    localStorage.removeItem('nova_user');
    localStorage.removeItem('nova_token');
    localStorage.clear(); // Clear everything to remove test data
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    signup,
    googleLogin,
    logout,
    isLoading,
    isAuthenticated: !!user && !!token,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};