import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest"
driver.get(url)
time.sleep(5)

for _ in range(5):  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

cards = driver.find_elements(By.CSS_SELECTOR, "div.rfq-card-module__card-box___qUC3r")

data = []
for card in cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, "div.rfq-card-module__title___2F7sT").text
    except:
        title = ""

    try:
        desc = card.find_element(By.CSS_SELECTOR, "div.rfq-card-module__desc___3Gndy").text
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
        buyer = card.find_element(By.CSS_SELECTOR, "div.rfq-card-module__buyer-name___F_R8p").text
    except:
        buyer = ""

    email_confirmed = "Yes" if "Email Confirmed" in card.text else "No"
    typically_replies = "Yes" if "Typically replies" in card.text else "No"

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


df = pd.DataFrame(data)
df.to_csv("rfq_data.csv", index=False, encoding='utf-8-sig')
print("Scraping complete. Data saved to rfq_data.csv")

driver.quit()

print(df.head(10))