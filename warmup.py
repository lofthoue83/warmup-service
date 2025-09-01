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
    Warm up the cache by fetching users and their profile images
    """
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print(f"[{datetime.now()}] ERROR: Missing environment variables")
        return
    
    # Query users directly from Supabase REST API
    users_url = f"{SUPABASE_URL}/rest/v1/alle_nutzer"
    
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }
    
    # Parameters for the query - using actual column names
    params = {
        "select": "*",  # Get all columns to see structure
        "limit": str(USER_COUNT)
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            print(f"[{datetime.now()}] Starting cache warmup for {USER_COUNT} users...")
            
            # Fetch users
            response = client.get(users_url, headers=headers, params=params)
            
            if response.status_code == 200:
                users = response.json()
                print(f"[{datetime.now()}] SUCCESS: Fetched {len(users)} users")
                
                # Warm up image cache by requesting each user's photos
                images_warmed = 0
                for user in users:
                    if user.get('photos') and isinstance(user['photos'], list):
                        for photo in user['photos']:
                            # Photos might be URLs directly or objects with URL property
                            photo_url = photo if isinstance(photo, str) else photo.get('url') if isinstance(photo, dict) else None
                            if photo_url and photo_url.startswith('http'):
                                try:
                                    # Just HEAD request to warm CDN cache
                                    img_response = client.head(photo_url, timeout=5.0)
                                    if img_response.status_code == 200:
                                        images_warmed += 1
                                except:
                                    pass  # Ignore individual image errors
                
                print(f"[{datetime.now()}] Warmed {images_warmed} images in CDN cache")
                print(f"[{datetime.now()}] Cache warmup completed successfully")
            else:
                print(f"[{datetime.now()}] ERROR: Status {response.status_code}")
                print(f"[{datetime.now()}] Response: {response.text}")
                
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {str(e)}")

if __name__ == "__main__":
    warmup_cache()