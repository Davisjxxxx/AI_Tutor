# backend/scheduler.py
import os
from typing import Optional
from twilio.rest import Client as TwilioClient
import structlog
from datetime import datetime, timezone

from .supa import supabase

log = structlog.get_logger()

_twilio_client: Optional[TwilioClient] = None

def get_twilio() -> Optional[TwilioClient]:
    global _twilio_client
    if _twilio_client:
        return _twilio_client
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    if not sid or not token:
        log.warning("Twilio credentials not configured. SMS features disabled.")
        return None
    _twilio_client = TwilioClient(sid, token)
    return _twilio_client

async def run_due_jobs():
    """
    This function is designed to be called by a Vercel Cron Job.
    It processes all due reminders in a single run.
    """
    client = get_twilio()
    if not client:
        return {"processed": 0, "reason": "Twilio not configured"}

    now = datetime.now(timezone.utc).isoformat()
    res = supabase.table("reminders").select("*").lte("next_run_at", now).eq("status", "active").execute()
    
    if not res.data:
        return {"processed": 0, "reason": "No reminders due"}

    count = 0
    for row in res.data:
        phone = row.get("phone")
        message = row["message"]
        reminder_id = row["id"]
        
        try:
            sms = client.messages.create(
                body=message,
                from_=os.getenv("TWILIO_FROM"),
                to=phone
            )
            log.info("SMS sent successfully", sid=sms.sid)
            count += 1
        except Exception as e:
            log.error("Failed to send SMS", phone=phone, error=e)

        # Update the reminder for the next run
        supabase.table("reminders").update({
            "last_sent_at": datetime.now(timezone.utc).isoformat(),
            "next_run_at": (datetime.now(timezone.utc) + datetime.timedelta(days=1)).isoformat() # Simple daily for now
        }).eq("id", reminder_id).execute()
        
    return {"processed": count}

# This function is for local development only and should not be called on Vercel
def start_scheduler():
    from apscheduler.schedulers.background import BackgroundScheduler
    
    IS_VERCEL = os.getenv("VERCEL") == "1"
    if os.getenv("ENABLE_SCHEDULER") == "1" and not IS_VERCEL:
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_due_jobs, 'interval', minutes=1)
        scheduler.start()
        log.info("Local background scheduler started.")