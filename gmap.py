import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from time import sleep
from random import uniform


# Proxy and user-agent settings
SCRAPEOPS_PROXY_API_KEY = "852c514d-15ea-4afb-991e-53088aaaeab1"
SCRAPEOPS_PROXY_URL = f"http://proxy.scrapeops.io:8000?api_key={SCRAPEOPS_PROXY_API_KEY}"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Chrome options setup
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--lang=en")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument(f"--proxy-server={SCRAPEOPS_PROXY_URL}")

# Initialize undetected ChromeDriver
service = Service(ChromeDriverManager(driver_version="132.0.6834.111").install())
driver = uc.Chrome(service=service, options=chrome_options)

base_url = "https://www.google.com/maps/search/restaurants+in+Los+Angeles,+CA,+USA/?hl=en"
driver.get(base_url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))

# Scroll Function
def scroll_page(driver, scrollable_div):
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    retries = 0
    
    while True:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)
        sleep(uniform(2.5, 4.5))
        
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        if new_height == last_height:
            retries += 1
            if retries > 3:
                break
        else:
            last_height = new_height
            retries = 0

scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
scroll_page(driver, scrollable_div)


# Collect all restaurant links
items_link = []
items = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.THOPZb.CpccDe a.hfpxzc')
for item in items:
    href = item.get_attribute("href")
    items_link.append(href)

print(f"Found {len(items_link)} restaurants.")

# Store scraped data
data_list = []

for link in items_link:
    driver.get(link)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    sleep(2)  

    data = {}   
    try:
        data['name'] = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf.lfPIob").text
    except:
        data['name'] = None

    try:
        data['address'] = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"] div.Io6YTe').text
    except:
        data['address'] = None

    try:
        data['website'] = driver.find_element(By.CSS_SELECTOR, 'a[data-item-id="authority"]').get_attribute("href")
    except:
        data['website'] = None

    try:
        data['phone_number'] = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id^="phone:tel:"] div.Io6YTe').text
    except:
        data['phone_number'] = None

    # Extract Reviews
    try:
        reviews_section = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[.//div[contains(text(), "Reviews")]]')))
        reviews_section.click()
        sleep(3)
        
        try:
            total_reviews_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="fontBodySmall" and contains(text(), "reviews")]'))).text
            data['total_reviews'] = int(''.join(filter(str.isdigit, total_reviews_text)))
            sleep(2)
        except:
            data['total_reviews'] = None

        try:
            sort_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Sort reviews")]')))
            sort_button.click()
                
            newest_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@role="menuitemradio" and contains(., "Newest")]')))
            newest_option.click()
            sleep(2)
        except:
            pass

        try:
            latest_review = driver.find_element(By.CSS_SELECTOR, 'div.jJc9Ad span.rsqaWe').text
            data['latest_review_date'] = latest_review
        except:
            data['latest_review_date'] = None

    except:
        data['total_reviews'] = None
        data['latest_review_date'] = None

    data_list.append(data)

# Close driver after all data is scraped
driver.quit()

# Convert to DataFrame and save to CSV
df = pd.DataFrame(data_list)
df.to_csv("restaurants_data_upgraded.csv", index=False)
print("Data saved to restaurants_data.csv")
