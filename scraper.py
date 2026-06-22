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
        "Content-Type": "application/json"
    }

    # Webseite laden
    response = requests.get("https://www.schwarzwald-tourismus.info/schwarzwald/dorfurlaub/herrischried-und-rickenbach/veranstaltungen")
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Wir suchen direkt nach dem JSON-LD Block
    script_tag = soup.find("script", type="application/ld+json")
    
    if script_tag:
        data = json.loads(script_tag.string)
        
        # Falls es eine Liste ist (manchmal ist es ein einzelnes Event, manchmal eine Liste)
        events = data if isinstance(data, list) else [data]
        
        for event in events:
            # Nur Events verarbeiten
            if event.get("@type") == "Event":
                name = event.get("name")
                # Datum extrahieren und das 'T' für die Datenbank lesbar machen
                start_date = event.get("startDate", "").split('T')[0] 
                
                payload = {
                    "name": name, 
                    "veranstalter": "Schwarzwald Tourismus",
                    "datum": start_date
                }
                
                # Senden an Supabase
                requests.post(f"{URL}/rest/v1/feste", headers=headers, json=payload)
                print(f"Importiert: {name} am {start_date}")

if __name__ == "__main__":
    run_import()
