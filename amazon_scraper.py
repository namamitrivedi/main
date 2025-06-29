import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Function to extract data from a single page
def extract_laptops_from_page(page):
    url = f"https://www.amazon.in/s?k=laptop&page={page}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to load page {page}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    laptops = []

    # Loop through each product block
    for item in soup.select(".s-main-slot .s-result-item"):
        title_tag = item.select_one("h2 a span")
        price_tag = item.select_one(".a-price-whole")
        review_tag = item.select_one(".a-icon-alt")

        if title_tag and price_tag:
            name = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True).replace(",", "")
            review = review_tag.get_text(strip=True) if review_tag else "No review"
            laptops.append({
                "Name": name,
                "Price (INR)": price,
                "Review": review
            })

    return laptops

# Collect data from first 5 pages
all_laptops = []
for page in range(1, 6):
    print(f"Scraping page {page}...")
    laptops = extract_laptops_from_page(page)
    all_laptops.extend(laptops)
    time.sleep(2)  # Sleep to avoid being blocked

# Save to CSV
df = pd.DataFrame(all_laptops)
df.to_csv("amazon_laptops.csv", index=False)
print("✅ Data saved to 'amazon_laptops.csv'")
