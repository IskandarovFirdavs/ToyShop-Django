from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from .models import ProductModel, BannerModel
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView



class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ProductModel.objects.all() 
        context['discounts'] = ProductModel.objects.order_by('-discount')[:3]
        context['banners'] = BannerModel.objects.filter(is_active=True)[:3]
        return context


    
class About(TemplateView):
    template_name = 'about.html'
    

class Order_history(TemplateView):
    template_name = 'order_history.html'
    
class ProductListView(TemplateView):
    model = ProductModel
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ProductModel.objects.all() 
        context['discounts'] = ProductModel.objects.order_by('-discount')[:3]
        context['banners'] = BannerModel.objects.filter(is_active=True)[:3]
        return context

    def get_queryset(self):
        qs = ProductModel.objects.all()

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)

        return qs



    
class ProductDetailView(DetailView):
    model = ProductModel
    template_name = 'product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related'] = self.object.category.products.exclude(pk=self.object.pk)[:4]
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.object
            comment.save()
            return redirect('products:product', pk=self.object.pk)   

        context['comment_form'] = form
        return self.render_to_response(context)

    
class WishlistListView(LoginRequiredMixin, ListView):
    template_name = 'wishlist.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return self.request.user.wishlist.order_by('-pk')


@login_required
def create_wishlist(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)

    if request.user in product.wishlist.all():
        product.wishlist.remove(request.user)

    else:
        product.wishlist.add(request.user)

    product.save()

    return redirect(request.GET.get('next', '/'))

@login_required
def add_all_to_cart(request):
    wishlist_items = request.user.wishlist.all()
    
    for product in wishlist_items:
        request.user.cart.add(product)

    return redirect('wishlist')


class CartListView(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return self.request.user.cart.order_by('-pk')


@login_required
def create_cart(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)

    if request.user in product.cart.all():
        product.cart.remove(request.user)

    else:
        product.cart.add(request.user)

    product.save()

    return redirect(request.GET.get('next', '/'))
