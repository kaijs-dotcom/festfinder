import os
import requests
from datetime import datetime

def run_cleanup():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    # Heute als Datum (im Format, das in deiner DB steht, z.B. ISO)
    today = datetime.now().strftime("%Y-%m-%d")
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    # Wir löschen alle Einträge, deren Datum kleiner als heute ist
    # WICHTIG: Das setzt voraus, dass du eine Spalte 'datum' hast.
    # Wenn du nur den Namen hast, können wir das aktuell nicht datumsbasiert filtern.
    print(f"Cleanup: Lösche Events vor dem {today}...")
    
    # DELETE-Aufruf an Supabase
    response = requests.delete(
        f"{url}/rest/v1/feste?datum=lt.{today}", 
        headers=headers
    )
    
    print(f"Cleanup abgeschlossen. Status: {response.status_code}")

if __name__ == "__main__":
    run_cleanup()
