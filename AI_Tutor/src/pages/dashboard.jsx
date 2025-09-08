import { sanitizeInput, validateReminderText } from '../utils/security.js';

const cleanText = sanitizeInput(newReminder);
if (!validateReminderText(cleanText)) return;
const { data, error } = await supabase
  .from('reminders')
  .insert([{ user_id: user.id, text: cleanText, done: false }])
  .select(); 