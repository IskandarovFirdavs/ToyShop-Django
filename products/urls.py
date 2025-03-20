from django.urls import path
from .views import Home, About, Cart, Order_history, ProductListView, ProductDetailView, Wishlist

app_name = 'products'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('cart/', Cart.as_view(), name='cart'),
    path('order_history/', Order_history.as_view(), name='order_history'),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('wishlist/', Wishlist.as_view(), name='wishlist'),
]