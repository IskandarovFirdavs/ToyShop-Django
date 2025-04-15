from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, ListView
from .models import ProductModel, BannerModel, CategoryModel, AgeModel
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin



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
    

class ProductListView(ListView):
    model = ProductModel
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 1
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discounts'] = ProductModel.objects.order_by('-discount')[:3]
        context['banners'] = BannerModel.objects.filter(is_active=True)[:3]
        context['categories'] = CategoryModel.objects.all()    
        context['selected_categories'] = self.request.GET.getlist('category')
        context['age_ranges'] = AgeModel.objects.all()     
        context['selected_age_ranges'] = self.request.GET.getlist('age_ranges')

        return context

    def get_queryset(self):    
        qs = ProductModel.objects.all()  

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
 
 
        #  Category filter
        cat = self.request.GET.get('cat')
        if cat:
            qs = qs.filter(category__id=cat)

        # sort
        sort = self.request.GET.get('sort')
        if sort:
            if sort == 'price':
                qs = sorted(qs, key=lambda i: i.get_price())
            elif sort == '-price':
                qs = sorted(qs, key=lambda i: i.get_price(), reverse=True)
            elif sort == '-created_at':
                qs = sorted(qs, key=lambda i: i.created_at(), reverse=True)
            


        #  Age range filter
        age_ranges = self.request.GET.get('age_ranges')
        if age_ranges:
            qs = qs.filter(agerange__id=age_ranges)

        #  Price filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            qs = qs.filter(price__gte=min_price, price__lte=max_price)

        # ↕ Sorting
        sort = self.request.GET.get('sort')
        if sort == 'price_low':
            qs = qs.order_by('price')
        elif sort == 'price_high':
            qs = qs.order_by('-price')
        elif sort == '-pk':
            qs = qs.order_by('-pk')  

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
