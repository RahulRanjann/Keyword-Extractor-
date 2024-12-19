from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def scrape_blog_posts(url):
    """
    Scrape blog posts from a given URL
    
    Args:
        url (str): The URL to scrape blog posts from
    
    Returns:
        list: List of scraped blog post dictionaries
    """
    # Set up Chrome WebDriver with headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # To run in headless mode
    service = Service(ChromeDriverManager().install())  # Set up the driver service

    # Initialize the driver using the Service and options
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)

        # Navigate to the initial page
        driver.get(url)

        # Wait and find blog post containers
        wait = WebDriverWait(driver, 10)
        blog_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.flex.flex-col > a'))
        )

        if not blog_elements:
            return []

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

        return results

    except Exception as e:
        print(f"Error in scraping: {str(e)}")
        return []

    finally:
        # Ensure driver is closed
        if driver:
            driver.quit()