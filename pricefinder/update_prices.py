def update_product_prices():
    """Fetches and updates prices for all stored products"""
    products = Product.objects.all()

    for product in products:
        new_price = scrape_price(product.url)

        if new_price:
            Price.objects.create(product=product, amount=new_price)
            print(f"Updated: {product.name} - KES {new_price}")
