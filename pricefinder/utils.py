import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures

def scrape_product_prices(search_query):
    """Scrapes multiple e-commerce websites and returns product prices"""
    search_urls = {
        "Jumia": f"https://www.jumia.co.ke/catalog/?q={search_query}",
        "Kilimall": f"https://www.kilimall.co.ke/search?q={search_query}",
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

                    products.append({
                        "store": store,
                        "name": product_name,
                        "price": float(cleaned_price) if cleaned_price else None,
                        "url": f"https://www.jumia.co.ke{product_link}"
                    })
            elif store == "Kilimall":
                response = requests.get(url)
                # Get all product containers
                product_elements = soup.select("div.product-item")
                for product in product_elements:
                    # Extract the product name
                    product_name = product.select_one("div.info-box p.product-title").text.strip()                 
                    # Extract the product price
                    product_price = product.select_one("div.info-box div.product-price").text.strip()                    
                    # Extract product link
                    product_link_tag = product.select_one("a")
                    product_link = product_link_tag['href']
                    product_link = f"https://www.kilimall.co.ke{product_link}"

                    
                    # Clean the price (if it's found)
                    cleaned_price = re.sub(r"[^\d.]", "", product_price) if product_price else None
                    
                    # Print product details (for debugging)
                    print(f"Found product: {product_name}, Price: {cleaned_price}, Link: {product_link}")
                    
                    # Append the product to the list
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
                product_elements = soup.select("div.card-info.list-card-layout__info")
                for product in product_elements:
                    product_name = product.select_one("h2.search-card-e-title").text.strip()
                    price_element = product.select_one("a.search-card-e-detail-wrapper")
                    product_price = price_element.text.strip() if price_element else None
                    product_link = product.select_one("a.search-card-e-detail-wrapper")['href']

                    if product_price:
                        price_match = re.search(r"([\d.,]+)-([\d.,]+)|([\d.,]+)", product_price)
                        if price_match:
                            if price_match.group(1) and price_match.group(2):
                                max_price = float(re.sub(r"[^\d.]", "", price_match.group(2)))
                                cleaned_price = max_price
                            elif price_match.group(3):
                                cleaned_price = float(re.sub(r"[^\d.]", "", price_match.group(3)))
                            else:
                                cleaned_price = None
                        else:
                            cleaned_price = None
                    else:
                        cleaned_price = None

                    products.append({
                        "store": store,
                        "name": product_name,
                        "price": cleaned_price,
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
