import json
import os
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username: str, json_output_path: str):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch contributions page, status code: {response.status_code}")
        
    soup = BeautifulSoup(response.text, "html.parser")
    days_data = []
    
    day_cells = soup.find_all("td", class_="ContributionCalendar-day")
    total_contributions = 0
    
    for cell in day_cells:
        date = cell.get("data-date")
        count_str = cell.get("data-count")
        level = cell.get("data-level", "0")
        
        if date and count_str is not None:
            count = int(count_str)
            total_contributions += count
            days_data.append({
                "date": date,
                "count": count,
                "level": int(level)
            })
            
    payload = {
        "total": total_contributions,
        "days": days_data
    }
    
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Fetched {len(days_data)} days of contributions. Total: {total_contributions}")

if __name__ == "__main__":
    fetch_contributions("Jeevanthchoudhary", "data/contributions.json")