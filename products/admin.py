from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import CategoryModel, ColorModel, ProductModel, BannerModel, CommentModel, ProductImageModel
from django.utils.translation import gettext_lazy as _


class MyTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(CategoryModel)
class CategoryModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['id']


@admin.register(ColorModel)
class ColorModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['id']


class ProductImageStackedInline(admin.TabularInline):
    model = ProductImageModel  
  


@admin.register(ProductModel)
class ProductModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'name', 'price', 'discount', 'category', 'is_available']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'is_available']
    ordering = ['id']
    inlines = [ProductImageStackedInline]

    def get_price(self, obj):
        return obj.get_price()

    get_price.short_description = _('Price')

@admin.register(BannerModel)
class BannerModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'description']
    search_fields = ['description']
    list_filter = ['description']
    ordering = ['id']


@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'created_at']
    search_fields = ['name', 'product__name']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
