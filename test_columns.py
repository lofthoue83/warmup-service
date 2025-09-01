#!/usr/bin/env python3
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

users_url = f"{SUPABASE_URL}/rest/v1/alle_nutzer"

headers = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
}

params = {
    "select": "*",
    "limit": "1"
}

with httpx.Client() as client:
    response = client.get(users_url, headers=headers, params=params)
    if response.status_code == 200:
        users = response.json()
        if users:
            print("Columns in alle_nutzer table:")
            for key in users[0].keys():
                print(f"  - {key}: {type(users[0][key]).__name__}")