from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def debug_scroll():
    o = Options()
    o.add_argument('--headless')
    o.add_argument('--window-size=1920,1080')
    o.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=o)
    
    url = 'https://www.flipkart.com/vebnor-solid-men-polo-neck-purple-t-shirt/product-reviews/itm4db4da97863b9?pid=TSHHDY8PK6ZMNEG8'
    print(f"Navigating to: {url}")
    driver.get(url)
    time.sleep(10)
    
    for i in range(10):
        # Count current visible review blocks
        # Strategy A: cPHDOP
        classic = len(driver.find_elements(By.CLASS_NAME, "cPHDOP"))
        # Strategy B: css-g5y9jx
        modern = len(driver.find_elements(By.CLASS_NAME, "css-g5y9jx"))
        
        print(f"Step {i}: Classic={classic}, Modern={modern}")
        
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5) # Give more time
        
        # Check for any "Next" or "Load more" buttons
        next_btns = driver.find_elements(By.XPATH, "//a[contains(., 'Next')] | //a[contains(@class, '_1LKsy1')] | //a[contains(@class, 'ge-49M')]")
        if next_btns:
            print(f"FOUND NEXT BUTTON: {next_btns[-1].text}")
            # If we find a Next button, then it's NOT infinite scroll, it's PAGINATION!
            # The user might be mistaken about it being single-page, or it's both.
            
    driver.quit()

if __name__ == "__main__":
    debug_scroll()
