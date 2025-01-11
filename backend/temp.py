from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route('/extract', methods=['GET'])
def extract_span_values():
    url = request.args.get('https://search17.quicksavesearch.com/roofing-jobs-can-make-up-to-2500-weekly-even-with-no-experience-heres-how-16067.webm?utm_medium=32_10&cpc=&section_id=%7Bplacement%7D&gkw=%7Bkeyword%7D&uid=&utm_campaign=arb-141245&click_id=EAIaIQobChMI8vnB7MKjzwIVEIppCh0oqQj0EAEYASAAEgLUMfD_BwE&network=google&utm_source=gg&ad_group_id=%7Badgroupid%7D&arb_campaign_id=141245&campaign_id=%7Bcampaignid%7D&ad_id=%7Bcreative%7D&arb_direct=on&_ckttl=91fbfcfd-4efb-4850-9ebe-05f7e9b6e292', default="", type=str)
    if not url:
        return jsonify({"error": "Please provide a valid URL."}), 400

    # Selenium WebDriver setup
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver_path = '/path/to/chromedriver'  # Update this path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Navigating to the URL...")
        driver.get(url)

        print("Waiting for iframe to load...")
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )
        print("Switching to iframe...")
        driver.switch_to.frame(iframe)

        print("Waiting for div elements with spans...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'div'))
        )

        print("Extracting spans inside divs...")
        span_values = []
        divs = driver.find_elements(By.TAG_NAME, 'div')
        for div in divs:
            spans = div.find_elements(By.TAG_NAME, 'span')
            for span in spans:
                span_values.append(span.text)
                print(f"Found span: {span.text}")

        print("Extraction complete.")
        return jsonify({"span_values": span_values})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
