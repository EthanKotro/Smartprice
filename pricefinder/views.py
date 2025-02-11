from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Product, Price
from .utils import scrape_product_price 

def product_search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        if search_query:
            try:
                # If it's a URL, attempt to scrape
                if search_query.startswith('http'):
                    product, created = Product.objects.get_or_create(url=search_query)
                    try:
                        current_price = scrape_product_price(search_query)
                        Price.objects.create(product=product, price=current_price)
                    except Exception as e: 
                        
                        print(f"Error scraping {search_query}: {e}")
                        messages.error(request, f"Error scraping price: {e}") 
                        return redirect('product_search') 

                
               
                return redirect('product_details', product_id=product.id) 
            except Exception as e: 
                messages.error(request, f"Error processing search: {e}") 
                return redirect('product_search') 

    return render(request, 'pricefinder/search.html') 

def product_details(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        prices = Price.objects.filter(product=product).order_by('-timestamp')
        context = {'product': product, 'prices': prices} 
        return render(request, 'pricefinder/details.html', context)
    except Product.DoesNotExist:
        raise Http404("Product not found.")
        
from django.shortcuts import render

def landing_page(request):
    return render(request, 'pricefinder/landing_page.html')       