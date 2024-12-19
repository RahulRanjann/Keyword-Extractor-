from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

def extract_keywords(url):
    """
    Extract keywords from a given URL using Selenium and BeautifulSoup
    
    Args:
        url (str): The URL to extract keywords from
    
    Returns:
        list: Extracted keywords
    """
    # Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Setup driver
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        
        # Find the container with related searches
        element_id = "relatedsearches1"
        container = driver.find_element(By.ID, element_id)
        
        # Find iframe
        iframe = container.find_element(By.TAG_NAME, "iframe")
        iframe_src = iframe.get_attribute("src")
        
        # Fetch iframe content
        response = requests.get(iframe_src)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract spans with specific class
            iframe_class_to_extract = "p_ si34 span"
            spans = soup.find_all("span", class_=iframe_class_to_extract)
            
            # Extract text from spans
            extracted_data = [span.get_text(strip=True) for span in spans]
            return extracted_data
        
        return []
    
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []
    
    finally:
        # Ensure driver is closed
        if driver:
            driver.quit()