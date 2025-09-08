// Security utilities for AURA web app

// Sanitize input to prevent XSS & limit length
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return '';
  return input.trim().replace(/[<>]/g, '').substring(0, 1000);
};

// Validate email format
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validate password strength (min 8 chars, upper, lower, digit)
export const validatePassword = (password) => {
  return password.length >= 8 && /[A-Z]/.test(password) && /[a-z]/.test(password) && /[0-9]/.test(password);
};

// Validate reminder text
export const validateReminderText = (text) => {
  const clean = sanitizeInput(text);
  return clean.length > 0 && clean.length <= 500;
};

// Simple client-side rate limiter
export const rateLimit = {
  attempts: new Map(),
  check: (key, max = 5, windowMs = 60_000) => {
    const now = Date.now();
    const arr = rateLimit.attempts.get(key) || [];
    const recent = arr.filter((t) => now - t < windowMs);
    if (recent.length >= max) return false;
    recent.push(now);
    rateLimit.attempts.set(key, recent);
    return true;
  },
}; 