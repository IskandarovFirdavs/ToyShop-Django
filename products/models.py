from django.db import models
from django.utils.translation import gettext_lazy as _

class CategoryModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    image = models.ImageField(upload_to='categories')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ColorModel(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('name'))

    def __str__(self):
        return self.name if self.name else "Unnamed color"

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'




class ProductModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.CharField(max_length=255, verbose_name=_("short description"))
    long_description = models.TextField(verbose_name=_("long description"))
    discount = models.IntegerField(default=0, verbose_name=_("discount"))
    image = models.ImageField(upload_to='products')
    extra_images = models.JSONField(default=list, verbose_name=_("extra images"))
    is_available = models.BooleanField(default=True, verbose_name=_("is_available"))
    availability = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='products')
    color = models.ForeignKey('ColorModel', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    age_range = models.CharField(max_length=10, null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
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




class BannerModel(models.Model):
    image = models.ImageField(upload_to='banners/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        
        


class CommentModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment {self.comment} by {self.name}'
