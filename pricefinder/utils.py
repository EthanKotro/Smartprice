from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import re


def scrape_product_prices(search_query):
    """Scrapes multiple e-commerce websites and returns product prices"""

    # Set Chrome options to avoid detection
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)

    search_urls = {
        "Jumia": f"https://www.jumia.co.ke/catalog/?q={search_query}",
        "Kilimall": f"https://www.kilimall.co.ke/search?search={search_query}",
        "Amazon Kenya": f"https://www.amazon.com/s?k={search_query}",
        "Alibaba": f"https://www.alibaba.com/trade/search?SearchText={search_query}",
    }

    products = []

    for store, url in search_urls.items():
        driver.get(url)
        time.sleep(random.uniform(3, 6))  # Delay to mimic human behavior

        try:
            if store == "Jumia":
                product_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "h3.name"))
                ).text
                product_price = driver.find_element(
                    By.CSS_SELECTOR, "div.prc").text
                product_link = driver.find_element(
                    By.CSS_SELECTOR, "a.core").get_attribute("href")

            elif store == "Kilimall":
                product_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "p.title"))
                ).text
                product_price = driver.find_element(
                    By.CSS_SELECTOR, "b.price").text
                product_link = driver.find_element(
                    By.CSS_SELECTOR, "a.product").get_attribute("href")

            elif store == "Amazon Kenya":
                product_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "span.a-size-medium"))
                ).text
                product_price = driver.find_element(
                    By.CSS_SELECTOR, "span.a-price-whole").text
                product_link = driver.find_element(
                    By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")

            elif store == "Alibaba":
                product_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "h2.title"))
                ).text
                product_price = driver.find_element(
                    By.CSS_SELECTOR, "span.price").text
                product_link = driver.find_element(
                    By.CSS_SELECTOR, "a.product").get_attribute("href")

            # Clean and convert price
            # Remove non-numeric characters
            cleaned_price = re.sub(r"[^\d.]", "", product_price)

            products.append({
                "store": store,
                "name": product_name,
                "price": float(cleaned_price) if cleaned_price else None,
                "url": product_link
            })

        except Exception as e:
            print(f"Error scraping {store}: {e}")

    driver.quit()
    return products


def get_best_deal(products):
    """Finds the cheapest product"""
    products = [p for p in products if p["price"]
                is not None]  # Remove None values
    if not products:
        return None
    return min(products, key=lambda x: x["price"])  # Find the lowest price
