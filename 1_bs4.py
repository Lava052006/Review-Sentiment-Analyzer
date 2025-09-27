import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# The direct URL to the reviews page
REVIEWS_URL = "https://www.flipkart.com/vibesle-pyrite-green-aventurine-citrine-golden-tiger-s-eye-citrine-7-chakra-clear-quartz-beads-agate-crystal-bracelet/product-reviews/itm9644f801bf83a?pid=BBAH8J6PCY8R2HW8&lid=LSTBBAH8J6PCY8R2HW8OGC6VY&marketplace=FLIPKART"

# You can change this to scrape more or fewer pages
MAX_PAGES = 10

def setup_driver():
    """Sets up the Selenium WebDriver."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_flipkart_reviews(reviews_url, max_pages):
    """
    Scrapes reviews from a Flipkart reviews page with updated selectors and robust waits.
    """
    driver = setup_driver()
    all_reviews = []
    
    print(f"Navigating to reviews page: {reviews_url}")
    driver.get(reviews_url)

    for page_num in range(max_pages):
        print(f"Scraping page {page_num + 1}...")
        
        # --- IMPROVEMENT: Wait for review content to be present ---
        try:
            # Wait a maximum of 10 seconds for the first review block to appear
            # The new class name for a review block is 'cPHDOP'
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cPHDOP"))
            )
        except TimeoutException:
            print("Content did not load in time. Ending scrape.")
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # --- FIX: Use the new, correct class name for review blocks ---
        review_blocks = soup.find_all('div', class_='cPHDOP')
        
        if not review_blocks:
            print("No review blocks found with the expected class. The website structure may have changed.")
            break
            
        for block in review_blocks:
            # --- FIX: Use the new, correct class for the review text ---
            review_text_element = block.find('div', class_='ZmyHeo')
            if review_text_element:
                review_text = review_text_element.get_text(strip=True)
                all_reviews.append(review_text)

        # --- Pagination Logic ---
        try:
            next_button = driver.find_element(By.XPATH, "//a/span[text()='Next']")
            driver.execute_script("arguments[0].click();", next_button)
        except NoSuchElementException:
            print("This is the last page of reviews.")
            break
            
    driver.quit()
    return all_reviews

print(f"Starting scraper for URL: {REVIEWS_URL}")
scraped_reviews = scrape_flipkart_reviews(REVIEWS_URL, max_pages=MAX_PAGES)

if scraped_reviews:
    print(f"\nSuccessfully scraped a total of {len(scraped_reviews)} reviews.")
    
    df = pd.DataFrame(scraped_reviews, columns=['review_text'])
    
    print("\n--- Sample of Scraped Reviews ---")
    print(df.head(10))
    
    # Optional: Save the results to a CSV file
    # df.to_csv('cmf_phone_reviews_final.csv', index=False)
    # print("\nSaved reviews to cmf_phone_reviews_final.csv")
else:
    print("\nNo reviews were scraped. Please check the URL and the script's selectors.")

