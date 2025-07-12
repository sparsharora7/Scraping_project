import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment to run without opening the browser
options.add_argument("--disable-blink-features=AutomationControlled")

# Start the Chrome browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Alibaba RFQ URL
url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest"
driver.get(url)
time.sleep(5)

# Wait for RFQ cards to appear
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rfq-card-module__card-box')]"))
    )
except:
    print("⛔ RFQ cards did not load in time.")
    driver.quit()
    exit()

# Scroll to load more RFQs (you can increase the range for more scrolling)
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Get RFQ cards
cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'rfq-card-module__card-box')]")
print(f"✅ Found {len(cards)} RFQ cards")

data = []
for card in cards:
    try:
        title = card.find_element(By.XPATH, ".//div[contains(@class, 'title')]").text
    except:
        title = ""

    try:
        desc = card.find_element(By.XPATH, ".//div[contains(@class, 'desc')]").text
    except:
        desc = ""

    try:
        quantity = card.find_element(By.XPATH, ".//span[contains(text(),'Quantity Required')]/following-sibling::span").text
    except:
        quantity = ""

    try:
        country = card.find_element(By.XPATH, ".//span[contains(text(),'Posted in:')]/following-sibling::span").text
    except:
        country = ""

    try:
        quotes = card.find_element(By.XPATH, ".//span[contains(text(),'Quotes Left')]/following-sibling::span").text
    except:
        quotes = ""

    try:
        date_posted = card.find_element(By.XPATH, ".//span[contains(text(),'Date Posted')]/following-sibling::span").text
    except:
        date_posted = ""

    try:
        buyer = card.find_element(By.XPATH, ".//div[contains(@class, 'buyer-name')]").text
    except:
        buyer = ""

    # Check badges
    card_text = card.text.lower()
    email_confirmed = "Yes" if "email confirmed" in card_text else "No"
    typically_replies = "Yes" if "typically replies" in card_text else "No"

    data.append({
        "Title": title,
        "Description": desc,
        "Quantity Required": quantity,
        "Country": country,
        "Quotes Left": quotes,
        "Date Posted": date_posted,
        "Buyer Name": buyer,
        "Email Confirmed": email_confirmed,
        "Typically Replies": typically_replies,
    })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("rfq_data.csv", index=False, encoding='utf-8-sig')

print("✅ Scraping complete. Data saved to rfq_data.csv")
driver.quit()
