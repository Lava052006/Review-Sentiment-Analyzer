import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re

def get_reviews_url(product_url):
    """Converts a standard Flipkart product URL to its reviews page URL."""
    if "product-reviews" in product_url:
        return product_url
    if "/p/" in product_url:
        return product_url.replace("/p/", "/product-reviews/")
    return product_url

def setup_driver():
    """Sets up a headless Chrome WebDriver."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_reviews(product_url, target_count=50):
    """Scrapes reviews from Flipkart using an Infinite-Scroll engine."""
    reviews_url = get_reviews_url(product_url)
    all_reviews = []
    seen_texts = set()
    
    driver = None
    try:
        driver = setup_driver()
        driver.get(reviews_url)
        time.sleep(5)

        scroll_attempts = 0
        max_scroll_attempts = 20
        
        while len(all_reviews) < target_count and scroll_attempts < max_scroll_attempts:
            # Scroll to load more
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            current_page_reviews = []

            # Strategy: Modern Layout (found in T-shirts, Electronics, etc.)
            row_containers = soup.find_all('div', class_='css-g5y9jx')
            for container in row_containers:
                text_divs = container.find_all('div', class_='css-146c3p1')
                if not text_divs: continue
                
                full_text = " ".join([d.get_text(separator=" ", strip=True) for d in text_divs])
                rating_match = re.search(r'(\d)\s*star', full_text, re.I)
                rating = rating_match.group(1) if rating_match else "3"
                
                # Clean up boilerplate
                clean_text = re.sub(r'Review for:.*?(Size|Color).*?(  |$)', '', full_text, flags=re.I)
                clean_text = re.sub(r'\d\s*star', '', clean_text, flags=re.I)
                
                # Strip Flipkart boilerplate
                boilerplate = [
                    r'Helpful\s*\d*', r'Report\s*abuse', r'Certified\s*Buyer', r'Permalink', 
                    r'Verified\s*Buyer', r'Most\s*Latest', r'Positive\s*Reviews', r'Negative\s*Reviews',
                    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*\d{4}',
                    r'\b[A-Z]{3,}\b'
                ]
                for pattern in boilerplate:
                    clean_text = re.sub(pattern, '', clean_text, flags=re.I)
                
                clean_text = clean_text.strip()
                if len(clean_text) > 5 and clean_text not in seen_texts:
                    current_page_reviews.append({'review': clean_text, 'rating': rating})
                    seen_texts.add(clean_text)

            if not current_page_reviews:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                all_reviews.extend(current_page_reviews)
            
    except Exception as e:
        print(f"Scraper error: {e}")
    finally:
        if driver: driver.quit()
            
    return pd.DataFrame(all_reviews[:target_count])
