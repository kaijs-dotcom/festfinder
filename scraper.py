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
    
    # JSON-LD finden
    script_tag = soup.find("script", type="application/ld+json")
    
    if script_tag:
        data = json.loads(script_tag.string)
        events = data if isinstance(data, list) else [data]
        
        for event in events:
            if event.get("@type") == "Event":
                name = event.get("name")
                raw_date = event.get("startDate", "Kein Datum")
                # Datum bereinigen (nimmt nur den Tag: 2026-06-25)
                clean_date = raw_date.split('T')[0] if 'T' in raw_date else raw_date
                
                payload = {
                    "name": name,
                    "veranstalter": "Schwarzwald Tourismus",
                    "datum": clean_date
                }
                
                # Senden an Supabase
                r = requests.post(f"{URL}/rest/v1/feste", headers=headers, json=payload)
                
                if r.status_code in [200, 201]:
                    print(f"Erfolg: '{name}' mit Datum '{clean_date}' wurde übertragen.")
                else:
                    print(f"FEHLER bei '{name}': Status {r.status_code} - {r.text}")

if __name__ == "__main__":
    run_import()
