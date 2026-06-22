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
    response = requests.get("https://www.schwarzwald-tourismus.info/schwarzwald/dorfurlaub/herrischried-und-rickenbach/veranstaltungen")
    soup = BeautifulSoup(response.content, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")
    
    if script_tag:
        data = json.loads(script_tag.string)
        events = data if isinstance(data, list) else [data]
        
        for event in events:
            if event.get("@type") == "Event":
                # Bereinigung
                name = event.get("name", "Unbekannt")
                raw_date = event.get("startDate", "1970-01-01")
                clean_date = raw_date.split('T')[0]
                
                # Payload erstellen
                payload = {
                    "name": name,
                    "veranstalter": "Schwarzwald Tourismus",
                    "datum": clean_date 
                }
                
                print(f"DEBUG: Sende Payload: {json.dumps(payload)}")
                
                # Senden
                r = requests.post(f"{URL}/rest/v1/feste", headers=headers, json=payload)
                
                # Antwort analysieren
                if r.status_code in [200, 201]:
                    print(f"ERFOLG: Supabase antwortet mit: {r.json()}")
                else:
                    print(f"FEHLER: {r.status_code} - {r.text}")

if __name__ == "__main__":
    run_import()
