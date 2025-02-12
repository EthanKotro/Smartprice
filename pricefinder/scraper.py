from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from .models import Product, Price


def scrape_price(product_url):
    """Scrapes price from a product page"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for efficiency
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    try:
        driver.get(product_url)
        time.sleep(2)  # Allow time for page to load

        if "jumia.co.ke" in product_url:
            price_element = driver.find_element(By.CLASS_NAME, "price")
        elif "kilimall" in product_url:
            price_element = driver.find_element(By.CLASS_NAME, "product-price")
        elif "amazon" in product_url:
            price_element = driver.find_element(By.ID, "priceblock_ourprice")
        elif "alibaba" in product_url:
            price_element = driver.find_element(
                By.CLASS_NAME, "price-container")
        else:
            raise Exception("Unsupported website")

        price_text = price_element.text.strip()
        # Extract digits
        price = float("".join(filter(str.isdigit, price_text)))
    except Exception as e:
        print(f"Error scraping {product_url}: {e}")
        price = None
    finally:
        driver.quit()

    return price
