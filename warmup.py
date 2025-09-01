#!/usr/bin/env python3
import httpx
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
USER_COUNT = int(os.getenv('USER_COUNT', '10'))

def warmup_cache():
    """
    Warm up the user cache by fetching users
    """
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print(f"[{datetime.now()}] ERROR: Missing environment variables")
        return
    
    edge_function_url = f"{SUPABASE_URL}/functions/v1/warmup-user-cache"
    
    headers = {
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "userCount": USER_COUNT
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            print(f"[{datetime.now()}] Starting cache warmup for {USER_COUNT} users...")
            response = client.post(edge_function_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"[{datetime.now()}] SUCCESS: Cache warmed with {result.get('usersWarmed', 0)} users")
                print(f"[{datetime.now()}] Cache valid until: {result.get('cacheValidUntil', 'unknown')}")
            else:
                print(f"[{datetime.now()}] ERROR: Status {response.status_code}")
                print(f"[{datetime.now()}] Response: {response.text}")
                
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {str(e)}")

if __name__ == "__main__":
    warmup_cache()