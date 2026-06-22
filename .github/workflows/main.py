import os
import requests
from bs4 import BeautifulSoup

def run_import():
    URL = os.environ.get("SUPABASE_URL")
    KEY = os.environ.get("SUPABASE_KEY")
    
    # Das ist der Header für das Upsert
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
            payload = {"name": name, "veranstalter": "Schwarzwald Tourismus"}
            
            # Upsert Befehl (statt DELETE + POST)
            requests.post(f"{URL}/rest/v1/feste", headers=headers, json=payload)

if __name__ == "__main__":
    run_import()
