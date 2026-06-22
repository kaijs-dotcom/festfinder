import os
import requests
import json
from bs4 import BeautifulSoup

def run_import():
    URL = os.environ.get("SUPABASE_URL")
    KEY = os.environ.get("SUPABASE_KEY")
    
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    # Webseite laden
    response = requests.get("https://www.schwarzwald-tourismus.info/veranstaltungen/die-salpeterer-tour-776ba42bdb")
    soup = BeautifulSoup(response.content, "html.parser")
    
    # JSON-LD extrahieren
    script_tag = soup.find("script", type="application/ld+json")
    
    if script_tag:
        try:
            data = json.loads(script_tag.string)
            # Falls es ein Dictionary ist, in eine Liste umwandeln
            event = data if isinstance(data, dict) else data[0]
            
            # Datum sauber extrahieren (nimmt den Teil vor dem 'T')
            raw_date = event.get("startDate", "1970-01-01")
            clean_date = raw_date.split('T')[0]
            
            payload = {
                "name": event.get("name"),
                "veranstalter": "Schwarzwald Tourismus",
                "datum": clean_date
            }
            
            # An Supabase senden
            r = requests.post(f"{URL}/rest/v1/feste", headers=headers, json=payload)
            if r.status_code == 201:
                print(f"Erfolg: {payload['name']} am {clean_date}")
            else:
                print(f"Fehler bei {payload['name']}: {r.text}")
                
        except Exception as e:
            print(f"Fehler beim Parsen: {e}")

if __name__ == "__main__":
    run_import()
