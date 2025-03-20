from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

class Home(TemplateView):
    template_name = 'index.html'
    
class About(TemplateView):
    template_name = 'about.html'
    
class Cart(TemplateView):
    template_name = 'cart.html'
    
class Order_history(TemplateView):
    template_name = 'order_history.html'
    
class ProductListView(TemplateView):
    template_name = 'shop.html'
    
class ProductDetailView(DetailView):
    template_name = 'product.html'
    
class Wishlist(TemplateView):
    template_name = 'wishlist.html'