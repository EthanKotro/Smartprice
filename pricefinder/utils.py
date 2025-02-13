import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures

def scrape_product_prices(search_query):
    """Scrapes multiple e-commerce websites and returns product prices"""

    search_urls = {
        "Jumia": f"https://www.jumia.co.ke/catalog/?q={search_query}",
        "Kilimall": f"https://www.kilimall.co.ke/search?search={search_query}",
        "Amazon Kenya": f"https://www.amazon.com/s?k={search_query}",
        "Alibaba": f"https://www.alibaba.com/trade/search?SearchText={search_query}",
    }

    products = []

    def scrape_store(store, url):
        """Scrapes an individual store"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            if store == "Jumia":
                product_elements = soup.select("div.info")
                for product in product_elements:
                    product_name = product.select_one("h3.name").text.strip()
                    product_price = product.select_one("div.prc").text.strip()
                    product_link_tag = product.find_parent("a")  # Find parent <a> tag
                    product_link = product_link_tag['href'] if product_link_tag else None

                    cleaned_price = re.sub(r"[^\d.]", "", product_price)
                    print(f"Found product: {product_name}, Price: {cleaned_price}, Link: {product_link}")

                    products.append({
                        "store": store,
                        "name": product_name,
                        "price": float(cleaned_price) if cleaned_price else None,
                        "url": f"https://www.jumia.co.ke{product_link}"
                    })

            elif store == "Kilimall":
                product_elements = soup.select("div.sku-product")
                for product in product_elements:
                    product_name = product.select_one("p.title").text.strip()
                    product_price = product.select_one("b.price").text.strip()
                    product_link = product.select_one("a.product")['href']

                    cleaned_price = re.sub(r"[^\d.]", "", product_price)

                    products.append({
                        "store": store,
                        "name": product_name,
                        "price": float(cleaned_price) if cleaned_price else None,
                        "url": product_link
                    })

            elif store == "Amazon Kenya":
                product_elements = soup.select("div.sku-product")
                for product in product_elements:
                    product_name = product.select_one("span.a-size-medium").text.strip()
                    product_price = product.select_one("span.a-price-whole").text.strip()
                    product_link = product.select_one("a.a-link-normal")['href']

                    cleaned_price = re.sub(r"[^\d.]", "", product_price)

                    products.append({
                        "store": store,
                        "name": product_name,
                        "price": float(cleaned_price) if cleaned_price else None,
                        "url": product_link
                    })



            elif store == "Alibaba":
                product_elements = soup.select("div.sku-product")
                for product in product_elements:
                    product_name = product.select_one("h2.title").text.strip()
                    product_price = product.select_one("span.price").text.strip()
                    product_link = product.select_one("a.product")['href']

                    cleaned_price = re.sub(r"[^\d.]", "", product_price)

                    products.append({
                        "store": store,
                        "name": product_name,
                        "price": float(cleaned_price) if cleaned_price else None,
                        "url": product_link
                    })
        except Exception as e:
            print(f"Error scraping {store}: {e}")

    # Use ThreadPoolExecutor to scrape stores in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for store, url in search_urls.items():
            futures.append(executor.submit(scrape_store, store, url))
        
        # Wait for all threads to finish
        concurrent.futures.wait(futures)

    return products



def get_best_deal(products):
    """Finds the cheapest product"""
    products = [p for p in products if p["price"]
                is not None]  # Remove None values
    if not products:
        return None
    return min(products, key=lambda x: x["price"])  # Find the lowest price
