import React, { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { useNavigate } from 'react-router-dom';
import AIChat from '../components/AIChat.jsx';
import MemoryVisualization from '../components/MemoryVisualization.jsx';

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);

export default function Dashboard() {
  const [reminders, setReminders] = useState([]);
  const [newReminder, setNewReminder] = useState('');
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('chat');
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchUserAndReminders() {
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);
      if (user) {
        const { data, error } = await supabase
          .from('reminders')
          .select('*')
          .eq('user_id', user.id)
          .order('id', { ascending: false });
        if (!error) setReminders(data);
      }
      setLoading(false);
    }
    fetchUserAndReminders();
  }, []);

  async function addReminder(e) {
    e.preventDefault();
    if (!newReminder.trim() || !user) return;
    const { data, error } = await supabase
      .from('reminders')
      .insert([{ user_id: user.id, text: newReminder, done: false }])
      .select();
    if (!error && data) setReminders([data[0], ...reminders]);
    setNewReminder('');
  }

  async function toggleDone(id, done) {
    await supabase.from('reminders').update({ done: !done }).eq('id', id);
    setReminders(reminders.map(r => r.id === id ? { ...r, done: !done } : r));
  }

  async function deleteReminder(id) {
    await supabase.from('reminders').delete().eq('id', id);
    setReminders(reminders.filter(r => r.id !== id));
  }

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    navigate('/');
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-zinc-900 to-indigo-950">
      {/* Header */}
      <header className="w-full bg-darkglass backdrop-blur border-b border-primary/20 p-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold text-primary">AURA Dashboard</h1>
          <div className="flex items-center gap-4">
            <span className="text-zinc-300">Welcome, {user?.email || 'User'}</span>
            <button
              onClick={handleSignOut}
              className="px-4 py-2 bg-glass rounded-lg text-zinc-300 hover:bg-primary/20 transition"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <div className="flex-1 max-w-6xl mx-auto w-full p-6">
        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-darkglass rounded-lg p-1">
            {[
              { id: 'chat', label: 'AI Tutor', icon: '🤖' },
              { id: 'reminders', label: 'Reminders', icon: '✅' },
              { id: 'memory', label: 'Memory', icon: '🧠' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-lg transition-all ${
                  activeTab === tab.id
                    ? 'bg-primary text-white shadow-glass'
                    : 'text-zinc-400 hover:text-white hover:bg-glass'
                }`}
              >
                <span>{tab.icon}</span>
                <span className="font-medium">{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Content Area */}
          <div className="lg:col-span-2">
            {activeTab === 'chat' && <AIChat user={user} />}
            
            {activeTab === 'reminders' && (
              <div className="bg-darkglass rounded-2xl p-8 shadow-glass backdrop-blur">
                <h2 className="text-2xl font-bold mb-4 text-primary">Reminders & Checkpoints</h2>
                <form onSubmit={addReminder} className="flex gap-2 mb-6">
                  <input
                    type="text"
                    placeholder="Add a new reminder or checkpoint..."
                    value={newReminder}
                    onChange={e => setNewReminder(e.target.value)}
                    className="flex-1 px-4 py-3 rounded-lg bg-glass text-white border border-primary focus:outline-none focus:ring-2 focus:ring-accent"
                  />
                  <button type="submit" className="px-6 py-3 rounded-lg bg-accent text-white font-bold shadow-glass hover:bg-primary transition">Add</button>
                </form>
                {loading ? (
                  <div className="text-zinc-400">Loading...</div>
                ) : reminders.length === 0 ? (
                  <div className="text-zinc-400">No reminders yet.</div>
                ) : (
                  <ul className="space-y-3">
                    {reminders.map(r => (
                      <li key={r.id} className="flex items-center justify-between bg-glass rounded-lg px-4 py-3 shadow-glass">
                        <div className="flex items-center gap-3">
                          <input
                            type="checkbox"
                            checked={r.done}
                            onChange={() => toggleDone(r.id, r.done)}
                            className="accent-primary w-5 h-5"
                          />
                          <span className={r.done ? 'line-through text-zinc-400' : 'text-white'}>{r.text}</span>
                        </div>
                        <button onClick={() => deleteReminder(r.id)} className="text-red-400 hover:text-red-600 font-bold ml-4">Delete</button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}

            {activeTab === 'memory' && <MemoryVisualization user={user} />}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="bg-darkglass rounded-2xl p-6 shadow-glass backdrop-blur">
              <h3 className="text-lg font-bold mb-4 text-accent">Quick Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-zinc-400">Active Reminders</span>
                  <span className="text-white font-semibold">
                    {reminders.filter(r => !r.done).length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-400">Completed Tasks</span>
                  <span className="text-white font-semibold">
                    {reminders.filter(r => r.done).length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-400">Learning Sessions</span>
                  <span className="text-white font-semibold">12</span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-darkglass rounded-2xl p-6 shadow-glass backdrop-blur">
              <h3 className="text-lg font-bold mb-4 text-primary">Quick Actions</h3>
              <div className="space-y-2">
                <button 
                  onClick={() => setActiveTab('chat')}
                  className="w-full px-4 py-2 bg-glass rounded-lg text-left text-zinc-300 hover:bg-primary/20 transition"
                >
                  💬 Ask AURA a question
                </button>
                <button 
                  onClick={() => setActiveTab('reminders')}
                  className="w-full px-4 py-2 bg-glass rounded-lg text-left text-zinc-300 hover:bg-primary/20 transition"
                >
                  ➕ Add reminder
                </button>
                <button 
                  onClick={() => setActiveTab('memory')}
                  className="w-full px-4 py-2 bg-glass rounded-lg text-left text-zinc-300 hover:bg-primary/20 transition"
                >
                  🧠 View memories
                </button>
              </div>
            </div>

            {/* Ad Slot */}
            <div className="bg-glass rounded-xl p-4 shadow-glass text-center text-zinc-400 border border-dashed border-accent">
              <span className="text-sm">Ad slot (support AURA or get Pro for ad-free!)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 