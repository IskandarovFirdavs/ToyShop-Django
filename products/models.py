from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    image = models.ImageField(upload_to='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class ColorModel(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("name"))

    def __str__(self):
        return self.name if self.name else _("Unnamed color")

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")


class ProductModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("price"))
    short_description = models.CharField(max_length=255, verbose_name=_("short description"))
    long_description = models.TextField(verbose_name=_("long description"))
    discount = models.IntegerField(default=0, verbose_name=_("discount"))
    image = models.ImageField(upload_to='products', verbose_name=_("image"))
    extra_images = models.JSONField(default=list, verbose_name=_("extra images"))
    is_available = models.BooleanField(default=True, verbose_name=_("is available"))
    availability = models.IntegerField(default=0, verbose_name=_("availability"))
    quantity = models.IntegerField(default=0, verbose_name=_("quantity"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, related_name='products', verbose_name=_("category")
    )
    color = models.ForeignKey(
        ColorModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name=_("color")
    )
    age_range = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("age range"))
    sku = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("SKU"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price

    def is_discounted(self):
        return self.discount > 0


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
