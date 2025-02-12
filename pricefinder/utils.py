from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_product_price(product_name, platform):
    """
    Scrapes the price of a product from the specified platform.

    Args:
        product_name (str): The name of the product.
        platform (str): The name of the e-commerce platform.

    Returns:
        float: The price of the product, or None if the price cannot be found.
    """

    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Navigate to the platform's homepage
        if platform == "jumia":
            driver.get("https://www.jumia.co.ke/") 
            # Jumia Search Logic
            search_box = driver.find_element(By.ID, "search-input") 
            search_box.send_keys(product_name)
            search_box.submit() 

            # Wait for search results to load 
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "prd_list")) 
            ) 

            # Find the first product result (you might need to refine this logic)
            product_link = driver.find_element(By.XPATH, "//div[@class='prd_list']/div[1]/a") 
            product_url = product_link.get_attribute('href') 
            driver.get(product_url) 

            # Extract price from the product page
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "prc")) 
            ) 
            price_text = price_element.text 
            price = float(price_text.replace('KSh', '').replace(',', '')) 

        elif platform == "amazon": 
            # Implement Amazon search logic here 
            pass 

        elif platform == "alibaba": 
            # Implement Alibaba search logic here 
            pass 

        elif platform == "kilimall": 
            # Implement Kilimall search logic here 
            pass 

        else:
            print(f"Unsupported website: {platform}")
            return None

    except Exception as e:
        print(f"Error scraping price from {platform} for {product_name}: {e}")
        return None

    finally:
        driver.quit()

    return price