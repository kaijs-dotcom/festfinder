import os
import requests
from bs4 import BeautifulSoup

def run_import():
    URL = os.environ.get("SUPABASE_URL")
    KEY = os.environ.get("SUPABASE_KEY")
    
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    # Webseite laden
    response = requests.get("https://www.schwarzwald-tourismus.info/schwarzwald/dorfurlaub/herrischried-und-rickenbach/veranstaltungen")
    soup = BeautifulSoup(response.content, "html.parser")
    
    # HIER: Dies ist der Selektor, der in V4 funktioniert hat. 
    # Wenn du ihn geändert hattest, ändere ihn zurück!
    events = soup.find_all("div", class_="c-headline__icon-wrapper")
    
    print(f"Gefundene Elemente: {len(events)}") # Debug-Ausgabe für das Log
    
    for event in events:
        h3 = event.find("h3")
        if h3:
            name = h3.get_text(strip=True)
            payload = {"name": name, "veranstalter": "Schwarzwald Tourismus"}
            
            response = requests.post(f"{URL}/rest/v1/feste", headers=headers, json=payload)
            print(f"Status {response.status_code} für {name}")

if __name__ == "__main__":
    run_import()
