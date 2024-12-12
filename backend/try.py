import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class SpecificIFrameExtractor:
    def __init__(self, url, target_id="master-1"):
        self.url = url
        self.target_id = target_id
        self.driver = None
        self.iframes = []

    def setup_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)

    def extract_specific_iframes(self):
        # Find iframes with specific ID
        iframes = self.driver.find_elements(By.ID, self.target_id)
        
        for iframe in iframes:
            iframe_info = {
                'src': iframe.get_attribute('src'),
                'name': iframe.get_attribute('name'),
                'id': iframe.get_attribute('id'),
                'class': iframe.get_attribute('class')
            }
            self.iframes.append(iframe_info)

    def save_iframes(self, filename='specific_iframes.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.iframes, f, indent=4, ensure_ascii=False)
        print(f"Found {len(self.iframes)} iframes with ID '{self.target_id}'")

    def run(self):
        try:
            self.setup_browser()
            self.extract_specific_iframes()
            self.save_iframes()
        finally:
            if self.driver:
                self.driver.quit()

def main():
    url = input("Enter webpage URL: ")
    extractor = SpecificIFrameExtractor(url)
    extractor.run()

if __name__ == "__main__":
    main()
