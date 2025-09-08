"""scheduler.py
Background scheduler that checks due reminders every minute and sends SMS via Twilio.
Stores SMS logs in `sms_log` table.
"""

import os
import asyncio
from datetime import datetime, timezone
import structlog

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from twilio.rest import Client as TwilioClient

from supa import supabase

log = structlog.get_logger()

load_dotenv()

TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

_twilio = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

async def process_due_reminders():
    now = datetime.now(timezone.utc).isoformat()
    # select reminders due now, status active
    res = supabase.table("reminders").select("*").lte("next_run_at", now).eq("status", "active").execute()
    if not res.data:
        return

    for row in res.data:
        phone = row.get("phone")
        message = row["message"]
        reminder_id = row["id"]
        tenant_id = row["tenant_id"]
        try:
            sms = _twilio.messages.create(body=message, from_=TWILIO_FROM, to=phone)
            supabase.table("sms_log").insert({
                "reminder_id": reminder_id,
                "tenant_id": tenant_id,
                "twilio_sid": sms.sid,
                "body": message,
                "sent_at": datetime.now(timezone.utc).isoformat()
            }).execute()
        except Exception as e:
            log.error("Failed to send SMS", phone=phone, error=e)

        # compute next_run_at (simple: add 1 day for now)
        supabase.table("reminders").update({
            "last_sent_at": datetime.now(timezone.utc).isoformat(),
            "next_run_at": datetime.now(timezone.utc).replace(hour= row["next_run_at"].hour, minute=row["next_run_at"].minute).isoformat()
        }).eq("id", reminder_id).execute()


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(process_due_reminders, CronTrigger(minute="*") )
    scheduler.start()
    log.info("Scheduler started for reminders.") 