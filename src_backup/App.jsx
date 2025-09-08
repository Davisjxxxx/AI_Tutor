import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/index.jsx';
import Login from './pages/login.jsx';
import Dashboard from './pages/dashboard.jsx';

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-indigo-950 text-white">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
} 