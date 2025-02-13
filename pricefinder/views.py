from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product
from .utils import get_best_deal, scrape_product_prices


def landing_page(request):
    """Renders the homepage"""
    return render(request, 'pricefinder/landing_page.html')


def product_search(request):
    query = request.GET.get('q', '').strip()  # Get the user's search term

    if not query:
        return render(request, 'pricefinder/search_results.html', {'query': query, 'products': []})

    # Scrape products from multiple sites
    scraped_data = scrape_product_prices(query)

    if not scraped_data:
        return render(request, 'pricefinder/search_results.html', {'query': query, 'products': []})

    best_deal = get_best_deal(scraped_data)  # Use AI to find the best deal

    return render(request, 'pricefinder/search_results.html', {'query': query, 'products': [best_deal]})


def product_details(request, product_id):
    """Displays product details"""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'pricefinder/product_details.html', {'product': product})


def best_deal_view(request):
    """API endpoint to return the best price for a searched product"""
    product_name = request.GET.get("q", "").strip()

    if not product_name:
        return JsonResponse({"error": "No product name provided"}, status=400)

    best_deal = get_best_deal(product_name)

    if best_deal:
        return JsonResponse(best_deal)

    return JsonResponse({"message": "No matching products found"}, status=404)
