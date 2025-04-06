from django.urls import path
from .views import Home, About, Order_history, ProductListView, ProductDetailView, WishlistListView, create_wishlist, add_all_to_cart,CartListView, create_cart

app_name = 'products'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('order_history/', Order_history.as_view(), name='order_history'),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('wishlist/', WishlistListView.as_view(), name="wishlist"),
    path("wishlist/<int:pk>/", create_wishlist, name="wishlist-create"),
    path("wishlist/add-all-to-cart/", add_all_to_cart, name="wishlist-add-all"),
    path('cart/', CartListView.as_view(), name="cart"),
    path("cart/<int:pk>/", create_cart, name="cart-create"),

]