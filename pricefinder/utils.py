import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
import numpy as np
from sklearn.linear_model import LinearRegression

# Dummy dataset for training the model
# Features: [normalized price, store credibility score]
# Labels: Predicted deal score (lower is better)
dummy_data = np.array([
    [0.8, 0.9, 1],  # Jumia
    [0.6, 0.8, 0.8],  # Kilimall
    [0.9, 0.95, 1.1],  # Amazon Kenya
    [0.5, 0.7, 0.7]  # Alibaba
])

X_train = dummy_data[:, :-1]
y_train = dummy_data[:, -1]

# Train the AI model
model = LinearRegression()
model.fit(X_train, y_train)


def scrape_product_prices(search_query):
    """Scrapes multiple e-commerce websites and returns product prices"""

    search_urls = {
        "Jumia": f"https://www.jumia.co.ke/catalog/?q={search_query}",
        "Kilimall": f"https://www.kilimall.co.ke/search?search={search_query}",
        "Amazon Kenya": f"https://www.amazon.com/s?k={search_query}",
        "Alibaba": f"https://www.alibaba.com/trade/search?SearchText={search_query}",
    }

    store_credibility = {
        "Jumia": 0.9,
        "Kilimall": 0.8,
        "Amazon Kenya": 0.95,
        "Alibaba": 0.7
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
                    product_link_tag = product.find_parent("a")
                    product_link = product_link_tag['href'] if product_link_tag else None
                    cleaned_price = re.sub(r"[^\d.]", "", product_price)

                    products.append({
                        "store": store,
                        "name": product_name,
                        "price": float(cleaned_price) if cleaned_price else None,
                        "url": f"https://www.jumia.co.ke{product_link}"
                    })
        except Exception as e:
            print(f"Error scraping {store}: {e}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_store, store, url)
                   for store, url in search_urls.items()]
        concurrent.futures.wait(futures)

    return products


def get_best_deal(products):
    """Finds the best deal using AI model"""
    if not products:
        return None

    store_credibility = {
        "Jumia": 0.9,
        "Kilimall": 0.8,
        "Amazon Kenya": 0.95,
        "Alibaba": 0.7
    }
    # Normalize prices
    prices = [p["price"] for p in products if p["price"] is not None]
    if not prices:
        return None
    max_price = max(prices)

    for product in products:
        if product["price"] is None:
            continue
        store_score = store_credibility.get(product["store"], 0.5)
        normalized_price = product["price"] / max_price
        score = model.predict([[normalized_price, store_score]])[0]
        product["deal_score"] = score

    return min(products, key=lambda x: x["deal_score"])
