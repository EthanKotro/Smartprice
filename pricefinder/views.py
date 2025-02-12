from django.shortcuts import render, redirect
from .models import Product, Price
from .utils import scrape_product_price 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def landing_page(request):
    return render(request, 'pricefinder/landing_page.html') 

def product_search(request):
    if request.method == 'POST':
        product_name = request.POST.get('search_query')

        # Create or retrieve the Product object
        product, created = Product.objects.get_or_create(name=product_name)

        # Platforms to scrape
        platforms = ["jumia", "amazon", "alibaba", "kilimall"] 

        for platform in platforms:
            try:
                price = scrape_product_price(product_name, platform) 
                if price:
                    Price.objects.create(product=product, price=price, source=platform) 
            except Exception as e:
                print(f"Error scraping price from {platform} for {product_name}: {e}")

        return redirect('pricefinder:product_details', product_id=product.id) 

    return render(request, 'pricefinder/landing_page.html') 

def product_details(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        prices = Price.objects.filter(product=product).order_by('price') 
        context = {'product': product, 'prices': prices} 
        return render(request, 'pricefinder/details.html', context)
    except Product.DoesNotExist:
        raise Http404("Product not found.")

def landing_page(request):
    return render(request, 'pricefinder/landing_page.html')       