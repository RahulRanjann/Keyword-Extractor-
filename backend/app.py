from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS
import time
import requests
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


class KeywordExtractor:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.element_id = "relatedsearches1"  # Use this ID consistently
        self.iframe_class_to_extract = "p_ si34 span"  # Class to search spans

    def setup_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get(self.url)

    def find_iframe_src_and_fetch_data(self):
        try:
            container = self.driver.find_element(By.ID, self.element_id)
            iframe = container.find_element(By.TAG_NAME, "iframe")
            iframe_src = iframe.get_attribute("src")

            # Fetch the iframe's HTML via requests
            response = requests.get(iframe_src)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                spans = soup.find_all("span", class_=self.iframe_class_to_extract)
                extracted_data = [span.get_text(strip=True) for span in spans]
                return extracted_data
            else:
                return []
        except Exception as e:
            print(f"Error extracting iframe src or data: {e}")
            return []

    def run(self):
        try:
            self.setup_browser()
            extracted_spans = self.find_iframe_src_and_fetch_data()
            return extracted_spans
        finally:
            if self.driver:
                self.driver.quit()


def fetch_and_parse_json(website_url):
    try:
        # Fetch the website content
        response = requests.get(website_url)
        
        # Check if the response is successful
        if response.status_code == 200:
            try:
                # Try parsing as JSON directly
                response_json = response.json()
                listOfKeyword = []
                # Assuming the path response_json.props.pageProps.keywords exists
                # Make sure you modify the path based on the actual JSON structure
                keywords = response_json.get('props', {}).get('pageProps', {}).get('keywords', [])
                return keywords
            except ValueError:
                # Parse the response as HTML to extract JSON
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Search for script tags that might contain JSON
                scripts = soup.find_all('script', type='application/json')
                
                if scripts:
                    # Extract the first JSON found
                    json_content = scripts[0].string.strip()
                    parsed_json = json.loads(json_content)
                    listOfKeyword = []
                    # Assuming the path response_json.props.pageProps.keywords exists
                    # Make sure you modify the path based on the actual JSON structure
                    keywords = parsed_json.get('props', {}).get('pageProps', {}).get('keywords', [])
                    
                    # if keywords:
                    #     for keyword in keywords:
                    #         listOfKeyword.append(keyword.get('name', 'Unknown'))
                        
                    #     return listOfKeyword
                    # else:
                    #     return "No keywords found in JSON."
                    return keywords
                else:
                    return "No JSON data found in the HTML."
        else:
            return f"Failed to fetch the URL. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

@app.route('/api/fetch', methods=['POST'])
def fetch_json_api():
    url = request.json.get('url')
    data = fetch_and_parse_json(url)
    return jsonify(data)



@app.route('/extract-keywords', methods=['POST'])
def extract_keywords():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "URL is required in the POST body"}), 400
        extractor = KeywordExtractor(url)
        keywords = extractor.run()
        return jsonify({"keywords": keywords}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Set up Chrome WebDriver with headless mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # To run in headless mode
        service = Service(ChromeDriverManager().install())  # Set up the driver service

        # Initialize the driver using the Service and options
        driver = webdriver.Chrome(service=service, options=options)

        # Navigate to the initial page
        driver.get(url)

        # Wait and find blog post containers
        wait = WebDriverWait(driver, 10)
        blog_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.flex.flex-col > a'))
        )

        if not blog_elements:
            driver.quit()
            return jsonify({"error": "No blog elements found"}), 404

        results = []
        for element in blog_elements:
            try:
                # Extract title
                title_elem = element.find_element(By.CSS_SELECTOR, 'h3.ant-typography')
                title = title_elem.text

                # Extract link
                link = element.get_attribute('href')

                # Extract image
                try:
                    image_elem = element.find_element(By.CSS_SELECTOR, 'img')
                    image = image_elem.get_attribute('src')
                    image_alt = image_elem.get_attribute('alt') or None
                except:
                    image = None
                    image_alt = None

                # Extract description
                try:
                    description_elem = element.find_element(By.CSS_SELECTOR, 'p.text-md')
                    description = description_elem.text
                except:
                    description = None

                results.append({
                    'title': title,
                    'link': link,
                    'image': image,
                    'image_alt': image_alt,
                    'description': description,
                    'keywords': []  # Initially empty, will be populated separately
                })

            except Exception as e:
                print(f"Error processing blog element: {e}")
                continue

        driver.quit()

        if results:
            return jsonify(results)
        else:
            return jsonify({"error": "No blog data found"}), 404

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the exception
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)