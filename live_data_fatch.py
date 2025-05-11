import requests
import json
import os
import time

# Function to fetch data from API and store only new entries in JSON file
def fetch_and_store_data():
    url = "https://91clubapi.com/api/webapi/GetNoaverageEmerdList"
    headers = {
        'Authorization': 'Bearer Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzQ2NTU2ODAxIiwibmJmIjoiMTc0NjU1NjgwMSIsImV4cCI6IjE3NDY1NTg2MDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI1LzcvMjAyNSAxMjo0MDowMSBBTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjIwNDA4MCIsIlVzZXJOYW1lIjoiOTE5OTUwMTQ1NzIzIiwiVXNlclBob3RvIjoiMSIsIk5pY2tOYW1lIjoiTWVtYmVyTk5HOUNCMDgiLCJBbW91bnQiOiIwLjQxIiwiSW50ZWdyYWwiOiIwIiwiTG9naW5NYXJrIjoiSDUiLCJMb2dpblRpbWUiOiI1LzcvMjAyNSAxMjoxMDowMSBBTSIsIkxvZ2luSVBBZGRyZXNzIjoiMjQwMTo0OTAwOmE5YzM6ZTJmZjpmNGIxOmIyZmY6ZmU1Mjo4ZDRhIiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIwIiwiS2V5Q29kZSI6IjY2MyIsIlRva2VuVHlwZSI6IkFjY2Vzc19Ub2tlbiIsIlBob25lVHlwZSI6IjEiLCJVc2VyVHlwZSI6IjAiLCJVc2VyTmFtZTIiOiJqYXlhcGFsbmltYmFyQGdtYWlsLmNvbSIsImlzcyI6Imp3dElzc3VlciIsImF1ZCI6ImxvdHRlcnlUaWNrZXQifQ.3LrVFNx5mp2Y51PuRg6HnF8VjBFmGJnV8rRlpO-jY68',
        'Content-Type': 'application/json'
    }
    data = {
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 1,
        "language": 0,
        "random": "edadfac48c3e424188403fb6a23c7fa2",
        "signature": "1329D74C90EE40A230707F5260C11F87",
        "timestamp": int(time.time())
    }

    try:
        res = requests.post(url, json=data, headers=headers)
        response_data = res.json()
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return

    # Extract and format new entries
    new_data = []
    for entry in response_data.get('data', {}).get('list', []):
        issue_number = entry.get('issueNumber')
        number = entry.get('number')
        colour = entry.get('colour')
        big_small = 'SMALL' if int(number) <= 4 else 'BIG'

        new_data.append({
            'Period Number': issue_number,
            'Number': number,
            'Colour': colour,
            'Big_Small': big_small
        })

    file_path = '/storage/emulated/0/AI_ML_MODEL/live_game_result.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Load previous data and extract period numbers
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_periods = {entry['Period Number'] for entry in existing_data}
    
    # Filter new entries to avoid duplicates
    unique_new_entries = [item for item in new_data if item['Period Number'] not in existing_periods]

    if unique_new_entries:
        # Combine and write back to file
        all_data = unique_new_entries + existing_data
        with open(file_path, 'w') as json_file:
            json.dump(all_data, json_file, indent=4)
        print(f"✅ {len(unique_new_entries)} new entries added. Total: {len(all_data)}")
    else:
        print("ℹ️ No new entries to add.")

# Run the function every 60 seconds
while True:
    fetch_and_store_data()
    time.sleep(60)
