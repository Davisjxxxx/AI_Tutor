"""supa.py
Central helper to instantiate a Supabase client with the service role key.
This runs on the server ONLY – never expose SERVICE_ROLE_KEY to the browser.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SERVICE_ROLE_KEY or SUPABASE_URL == "your_supabase_url_here":
    print("WARNING: SUPABASE_URL and SERVICE_ROLE_KEY not configured - reminder features disabled")
    supabase = None
else:
    try:
        supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    except Exception as e:
        print(f"WARNING: Failed to initialize Supabase: {e} - reminder features disabled")
        supabase = None 