"""aura_motivation_coach.py
Lightweight helper to send motivational SMS messages using Twilio.
Run as a one-off:
    python aura_motivation_coach.py --to +15551234567 --msg "You got this! One small step right now. 💪"
The long-term plan is to import `send_sms` from this module and schedule calls
with the `schedule` library or any async task runner.
"""

import os
import argparse
from dotenv import load_dotenv
from twilio.rest import Client
import schedule
import threading
import time
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")  # the Twilio phone number in E.164 format

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM]):
    raise EnvironmentError(
        "Missing one or more Twilio variables in .env: "
        "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM"
    )

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

def send_sms(to: str, message: str) -> str:
    """Send an SMS and return the Twilio message SID."""
    msg = client.messages.create(
        body=message,
        from_=TWILIO_FROM,
        to=to,
    )
    return msg.sid

# ---------------------------------------------------------------------------
# CLI entry point (for quick manual tests)
# ---------------------------------------------------------------------------


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Send a motivational SMS via Twilio")
    parser.add_argument("--to", required=True, help="Destination phone number in E.164 format, e.g. +15551234567")
    parser.add_argument(
        "--msg",
        default="You've got this! One tiny step forward right now.",
        help="Message text to send",
    )
    args = parser.parse_args()

    sid = send_sms(args.to, args.msg)
    print(f"✅ SMS sent. Twilio SID: {sid}")


if __name__ == "__main__":
    _cli()

# ---------------------------------------------------------------------------
# Scheduling helpers
# ---------------------------------------------------------------------------


def _run_schedule_forever():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start background thread once at import time
_scheduler_thread_started = False


def _ensure_scheduler_running():
    global _scheduler_thread_started
    if not _scheduler_thread_started:
        thread = threading.Thread(target=_run_schedule_forever, daemon=True)
        thread.start()
        _scheduler_thread_started = True


def schedule_sms_in(delay_minutes: int, to: str, message: str) -> None:
    """Schedule an SMS to be sent after `delay_minutes`."""

    def job():
        try:
            send_sms(to, message)
        except Exception as e:
            print(f"[SCHEDULER] Failed to send SMS: {e}")

    schedule.every(delay_minutes).minutes.do(job).tag("aura_coach")
    _ensure_scheduler_running()


def schedule_sms_at(target_time: datetime, to: str, message: str) -> None:
    """Schedule an SMS at an absolute datetime."""
    now = datetime.now()
    delay = (target_time - now).total_seconds() / 60
    if delay <= 0:
        raise ValueError("Target time must be in the future")
    schedule_sms_in(int(delay), to, message) 