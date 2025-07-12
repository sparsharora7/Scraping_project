# Alibaba RFQ Scraper (Python + Selenium)

This project is a web scraper built using **Python, Selenium**, and **Pandas** to extract RFQ (Request for Quotation) listings from [Alibaba's RFQ page](https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&tracelog=newest).

## ⚙️ Features
- Scrolls through multiple pages of RFQ listings
- Extracts key details like title, description, quantity, country, buyer, and more
- Saves the data into a `rfq_data.csv` file

## 📂 Output
The script creates a CSV file containing the scraped data:


## ⚠️ Important Note

> **The `rfq_data.csv` file may appear empty if you're not signed in to Alibaba.**

Alibaba now requires users to be **logged in** to view or interact with RFQ listings. Since Selenium runs a fresh browser session, it does not inherit your login state unless explicitly programmed.

### 🔐 Why the CSV Is Empty

- When not signed in, Alibaba may **block access** to RFQ content or redirect to a login prompt.
- As a result, no data is available to scrape, and the CSV remains empty.

## ✅ Next Steps (To Enable Scraping)

To make this script work fully:
- **Option 1:** Automate Alibaba login using Selenium.
- **Option 2:** Manually log in and inject session cookies into Selenium.
- **Option 3:** Use authenticated API access if available (unlikely for public RFQs).

Feel free to fork this project and enhance it with login/session support!


