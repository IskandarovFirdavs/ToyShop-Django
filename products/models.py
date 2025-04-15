from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from users.models import UserModel as User

class CategoryModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class AgeModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=("name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Age")
        verbose_name_plural = ("Ages")


class ColorModel(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("name"))

    def __str__(self):
        return self.name if self.name else _("Unnamed color")

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

class ProductModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    price = models.IntegerField(default=0, verbose_name=_("price"))
    discount = models.IntegerField(default=0, verbose_name=_("discount"))
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_("category"))
    color = models.ManyToManyField(ColorModel, related_name='products', verbose_name=_("color"))
    short_description = models.TextField(verbose_name=_("short_description"))
    long_description = models.TextField(verbose_name=_("long_description"))
    image = models.ImageField(upload_to='products/', verbose_name=_("image"))
    is_available = models.BooleanField(default=True, verbose_name=_("is_available"))
    agerange = models.ManyToManyField(AgeModel, related_name='products', verbose_name=("age_range"))
    wishlist = models.ManyToManyField(
        User,
        related_name='wishlist',
        verbose_name=_("wishlist"),
        null=True,
        blank=True,
    )
   
    cart = models.ManyToManyField(
        User,
        related_name='cart',
        verbose_name=_("cart"),
         null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price

    def is_discounted(self):
        return self.discount > 0




@login_required
def create_wishlist(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)

    if request.user in product.wishlist.all():
        product.wishlist.remove(request.user)

    else:
        product.wishlist.add(request.user)

    product.save()

    return redirect(request.GET.get('next', '/'))




class ProductImageModel(models.Model):
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name='images', verbose_name=_("product")
    )
    image = models.ImageField(upload_to='products/', verbose_name=_("image"))


    def __str__(self):
        return self.image.url if self.image else _("No Image")

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")



class BannerModel(models.Model):
    image = models.ImageField(upload_to='banners/', null=True, blank=True, verbose_name=_("image"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    description = models.TextField(verbose_name=_("description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    def __str__(self):
        return self.image.url if self.image else _("No Image")

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")


class CommentModel(models.Model):
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name='comments', verbose_name=_("product")
    )
    name = models.CharField(max_length=100, verbose_name=_("name"))
    comment = models.TextField(verbose_name=_("comment"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    def __str__(self):
        return f'Comment {self.comment} by {self.name}'

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
