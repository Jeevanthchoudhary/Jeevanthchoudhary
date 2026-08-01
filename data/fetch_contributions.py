import os
import json
from bs4 import BeautifulSoup
import urllib.request

def fetch_contributions():
    url = "https://github.com/users/Jeevanthchoudhary/contributions"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching contributions: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all contribution days
    days = soup.find_all('td', class_='ContributionCalendar-day')
    
    contributions = []
    for day in days:
        date = day.get('data-date')
        count_text = day.get('data-count')
        level = day.get('data-level')
        
        if date:
            contributions.append({
                'date': date,
                'count': int(count_text) if count_text else 0,
                'level': int(level) if level else 0
            })
            
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    output_path = 'data/contributions.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(contributions, f, indent=2)
        
    print(f"Successfully saved {len(contributions)} days of contributions to {output_path}")

if __name__ == '__main__':
    fetch_contributions()