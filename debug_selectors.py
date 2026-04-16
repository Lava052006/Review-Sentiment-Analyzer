from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def debug():
    o = Options()
    o.add_argument('--headless')
    o.add_argument('--window-size=1920,1080')
    o.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=o)
    
    url = 'https://www.flipkart.com/vebnor-solid-men-polo-neck-purple-t-shirt/product-reviews/itm4db4da97863b9?pid=TSHHDY8PK6ZMNEG8&lid=LSTTSHHDY8PK6ZMNEG8QBMR32'
    print(f"Navigating to: {url}")
    driver.get(url)
    time.sleep(10)
    
    print("\n--- Potential Next Buttons ---")
    # Search for anything that says "Next" or has pagination classes
    # ge-49M is a common flipkart pagination class
    # _1LKsy1 is another one
    nav_elements = driver.find_elements(By.XPATH, "//a | //span | //div")
    for el in nav_elements:
        try:
            text = el.text.strip()
            if text and ("Next" in text or "NEXT" in text or "next" in text):
                print(f"TAG: {el.tag_name} | CLASS: {el.get_attribute('class')} | TEXT: {text} | href: {el.get_attribute('href')}")
        except:
            continue

    driver.quit()

if __name__ == "__main__":
    debug()
