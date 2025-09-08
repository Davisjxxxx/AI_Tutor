import React, { useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { useNavigate } from 'react-router-dom';

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleAuth(e) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      let result;
      if (isSignUp) {
        result = await supabase.auth.signUp({ email, password });
      } else {
        result = await supabase.auth.signInWithPassword({ email, password });
      }
      if (result.error) throw result.error;
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  }

  const handleDemoLogin = async () => {
    setError('');
    setLoading(true);
    try {
      // Use a demo account for testing
      const demoEmail = 'demo@aura.ai';
      const demoPassword = 'demo123456';
      
      let result = await supabase.auth.signInWithPassword({ 
        email: demoEmail, 
        password: demoPassword 
      });
      
      if (result.error && result.error.message.includes('Invalid login credentials')) {
        // Try to create demo account if it doesn't exist
        result = await supabase.auth.signUp({ 
          email: demoEmail, 
          password: demoPassword 
        });
      }
      
      if (result.error) throw result.error;
      navigate('/dashboard');
    } catch (error) {
      setError('Demo mode error: ' + error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-gradient-to-br from-zinc-900 to-indigo-950">
      <form onSubmit={handleAuth} className="bg-darkglass rounded-2xl p-8 shadow-glass w-full max-w-md backdrop-blur">
        <h2 className="text-2xl font-bold mb-6 text-center text-primary">{isSignUp ? 'Sign Up' : 'Login'} to AURA</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="w-full mb-4 px-4 py-3 rounded-lg bg-glass text-white border border-primary focus:outline-none focus:ring-2 focus:ring-accent"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="w-full mb-4 px-4 py-3 rounded-lg bg-glass text-white border border-primary focus:outline-none focus:ring-2 focus:ring-accent"
          required
        />
        {error && <div className="mb-4 text-red-400 text-sm text-center">{error}</div>}
        <button
          type="submit"
          className="w-full py-3 rounded-lg bg-primary text-white font-bold shadow-glass hover:bg-accent transition mb-4"
          disabled={loading}
        >
          {loading ? (isSignUp ? 'Signing Up...' : 'Logging In...') : (isSignUp ? 'Sign Up' : 'Login')}
        </button>
        
        <div className="mb-4">
          <div className="text-center text-zinc-400 text-sm mb-2">or</div>
          <button
            type="button"
            onClick={handleDemoLogin}
            className="w-full py-3 rounded-lg bg-glass text-zinc-300 font-bold border border-accent hover:bg-accent/20 transition"
            disabled={loading}
          >
            {loading ? 'Connecting to Demo...' : 'Try Demo Account'}
          </button>
        </div>
        
        <div className="text-center text-zinc-300">
          {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
          <button
            type="button"
            className="text-accent underline ml-1"
            onClick={() => setIsSignUp(!isSignUp)}
          >
            {isSignUp ? 'Login' : 'Sign Up'}
          </button>
        </div>
      </form>
    </div>
  );
} 