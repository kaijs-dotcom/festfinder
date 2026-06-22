import os
import requests
from datetime import datetime

def run_cleanup():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    today = datetime.now().strftime("%Y-%m-%d")
    
    headers = {"apikey": key, "Authorization": f"Bearer {key}"}
    
    # Löscht alles, was VOR heute ist
    requests.delete(f"{url}/rest/v1/feste?datum=lt.{today}", headers=headers)

if __name__ == "__main__":
    run_cleanup()
