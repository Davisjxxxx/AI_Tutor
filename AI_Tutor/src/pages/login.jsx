import { validateEmail, validatePassword, rateLimit } from '../utils/security.js';

if (!validateEmail(email)) { setError('Invalid email format'); setLoading(false); return; }
if (!validatePassword(password)) { setError('Password must be 8+ chars with upper, lower, number'); setLoading(false); return; }
if (!rateLimit.check(email)) { setError('Too many attempts, please wait a minute'); setLoading(false); return; } 