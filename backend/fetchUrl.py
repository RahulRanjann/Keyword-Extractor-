import requests
import json

from bs4 import BeautifulSoup

def fetch_and_parse_json(website_url, output_file="response.json"):
    try:
        # Fetch the website content
        response = requests.get(website_url)
        
        # Check if the response is successful
        if response.status_code == 200:
            try:
                print()
                # Try parsing as JSON directly
                response_json = response.json()
                save_json(response_json, output_file)
            except ValueError:
                # Parse the response as HTML to extract JSON
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Search for script tags that might contain JSON
                scripts = soup.find_all('script', type='application/json')
                
                if scripts:
                    # Extract the first JSON found
                    json_content = scripts[0].string.strip()
                    parsed_json = json.loads(json_content)
                    
                    keywords = parsed_json['props']['pageProps']['keywords']
                
                    save_json(parsed_json, output_file)
                else:
                    print("No JSON data found in the HTML.")
        else:
            print(f"Failed to fetch the URL. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def save_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"JSON response saved to {output_file}")

# Input URL
# url = input("Enter the website URL: ")                 
url = 'https://fastanswershere.com/pick-up-truck-a-versatile-vehicle-for-every-need'
fetch_and_parse_json(url)



