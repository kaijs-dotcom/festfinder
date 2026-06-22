import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_import():
    URL = os.environ.get("SUPABASE_URL")
    KEY = os.environ.get("SUPABASE_KEY")
    
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    response = requests.get("https://www.schwarzwald-tourismus.info/schwarzwald/dorfurlaub/herrischried-und-rickenbach/veranstaltungen")
    soup = BeautifulSoup(response.content, "html.parser")
    
    events = soup.find_all("div", class_="c-headline__icon-wrapper")
    
    for event in events:
        h3 = event.find("h3")
        if h3:
            name = h3.get_text(strip=True)
            # HIER: Falls du das Datum aus einem HTML-Tag lesen kannst, ersetze es hier:
            # datum = event.find("span", class_="dein-datum-tag").text 
            datum = datetime.now().strftime("%Y-%m-%d") # Platzhalter-Datum
            
            payload = {
                "name": name, 
                "veranstalter": "Schwarzwald Tourismus",
                "datum": datum
            }
            requests.post(f"{URL}/rest/v1/feste", headers=headers, json=payload)

if __name__ == "__main__":
    run_import()
