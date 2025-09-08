import React from 'react';
import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-gradient-to-br from-zinc-900 to-indigo-950">
      {/* Hero Section */}
      <section className="w-full max-w-3xl text-center py-16 px-4">
        <h1 className="text-5xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent drop-shadow-lg">AURA</h1>
        <p className="text-xl mb-6 text-zinc-200">The context-aware, memory-driven AI assistant for <span className="text-accent font-semibold">learners</span> and <span className="text-primary font-semibold">neurodivergent minds</span>.</p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <Link to="/login" className="px-6 py-3 rounded-lg bg-primary text-white font-bold shadow-glass hover:bg-accent transition">Sign Up / Login</Link>
          <a href="#beta" className="px-6 py-3 rounded-lg bg-glass text-white font-bold shadow-glass border border-primary hover:bg-primary/80 transition backdrop-blur">Beta Offer</a>
        </div>
      </section>

      {/* Features */}
      <section className="w-full max-w-4xl grid md:grid-cols-3 gap-8 py-8 px-4">
        <div className="bg-darkglass rounded-xl p-6 shadow-glass backdrop-blur">
          <h2 className="text-lg font-bold mb-2 text-primary">Remembers You</h2>
          <p className="text-zinc-200">AURA keeps track of your learning, projects, and goals—so you never lose context, even after a break.</p>
        </div>
        <div className="bg-darkglass rounded-xl p-6 shadow-glass backdrop-blur">
          <h2 className="text-lg font-bold mb-2 text-accent">Adapts to Your Mind</h2>
          <p className="text-zinc-200">Whether you need step-by-step help, quick code, or gentle reminders, AURA adapts to your style and energy.</p>
        </div>
        <div className="bg-darkglass rounded-xl p-6 shadow-glass backdrop-blur">
          <h2 className="text-lg font-bold mb-2 text-primary">Built for Neurodivergence</h2>
          <p className="text-zinc-200">Designed for ADHD, dyslexia, and all learning styles—AURA helps you focus, recall, and thrive.</p>
        </div>
      </section>

      {/* Beta Offer */}
      <section id="beta" className="w-full max-w-2xl text-center py-12 px-4">
        <div className="bg-glass rounded-2xl p-8 shadow-glass border border-primary backdrop-blur">
          <h3 className="text-2xl font-bold mb-2 text-primary">Founding Beta: 50% Off for 6 Months</h3>
          <p className="mb-4 text-zinc-200">Join now and help shape the future of adaptive AI. Early users get exclusive pricing and direct input into new features.</p>
          <Link to="/login" className="px-6 py-3 rounded-lg bg-accent text-white font-bold shadow-glass hover:bg-primary transition">Claim Beta Access</Link>
        </div>
      </section>

      {/* Testimonials */}
      <section className="w-full max-w-4xl py-8 px-4">
        <h4 className="text-xl font-bold text-center mb-6 text-zinc-100">What Early Users Say</h4>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-darkglass rounded-xl p-6 shadow-glass backdrop-blur">
            <p className="italic text-zinc-200">“AURA remembered my study goals from weeks ago and helped me stay on track.”</p>
            <span className="block mt-2 text-zinc-400 text-sm">— College Student</span>
          </div>
          <div className="bg-darkglass rounded-xl p-6 shadow-glass backdrop-blur">
            <p className="italic text-zinc-200">“Finally, an AI that adapts to my ADHD workflow instead of fighting it.”</p>
            <span className="block mt-2 text-zinc-400 text-sm">— Indie Developer</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full text-center py-6 text-zinc-500 text-sm mt-8">
        Made with <span className="text-primary">♥</span> for learners & neurodivergent minds — AURA Beta
      </footer>
    </div>
  );
} 