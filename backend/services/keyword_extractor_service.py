from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

def extract_keywords():
    url = "https://search17.soamaps.com/los-autos-embargados-no-vendidos-se-venden-por-casi-nada-echar-un-vistazo-15632.webm?network=google&section_id=%7Bplacement%7D&arb_campaign_id=141216&utm_source=gg&campaign_id=%7Bcampaignid%7D&click_id=EAIaIQobChMI8vnB7MKjzwIVEIppCh0oqQj0EAEYASAAEgLUMfD_BwE&ad_id=%7Bcreative%7D&arb_direct=on&gkw=%7Bkeyword%7D&uid=&utm_medium=&cpc=&utm_campaign=arb-141216&ad_group_id=%7Badgroupid%7D&_ckttl=3f80b796-2fa5-4f8d-80ca-c1f02386f200"
    """
    Extract keywords from a given URL using Selenium and BeautifulSoup
    
    Args:
        url (str): The URL to extract keywords from
    
    Returns:
        list: Extracted keywords
    """
    # Chrome options for headless browsing
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Setup driver
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        
        # Find the container with related searches
        element_id = "/html/body/div/div/div/div/main/article/div[2]" # relatedsearches1
        container = driver.find_element(By.XPATH, element_id)
        print("line 36 container", container)
        icont = container.get_attribute("src")
        print("line 38 icont", icont)
        
        
        # Find iframe
        iframe = container.find_element(By.TAG_NAME, "iframe")
        print("line 39 iframe", iframe)
        iframe_src = iframe.get_attribute("src")
        
        # Fetch iframe content
        response = requests.get(iframe_src)
        print("line 43 response", response)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract spans with specific class
            iframe_class_to_extract = "p_ si34 span"
            spans = soup.find_all("span", class_=iframe_class_to_extract)
            
            # Extract text from spans
            extracted_data = [span.get_text(strip=True) for span in spans]
            print("line 53 extracted_data",extracted_data)
            return extracted_data
        
        return []
    
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []
    
    finally:
        # Ensure driver is closed
        if driver:
            driver.quit()