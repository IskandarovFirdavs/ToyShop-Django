from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import CategoryModel, ColorModel, ProductModel, BannerModel

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


@admin.register(ColorModel)
class ColorModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']
    
    
@admin.register(ProductModel)
class ProductModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'name', 'price', 'category', 'color', 'is_available']
    search_fields = ['name', 'category__name', 'color__name']
    list_filter = ['category', 'color', 'is_available']
    autocomplete_fields = ['category', 'color']
    readonly_fields = ['created_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'short_description', 'long_description', 'discount', 'image', 'extra_images', 'is_available', 'availability', 'quantity', 'category', 'color', 'age_range', 'sku')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['id']
    actions = ['make_available', 'make_unavailable']
    
    def make_available(self, request, queryset):
        queryset.update(is_available=True)
    make_available.short_description = 'Mark selected products as available'
    
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    make_unavailable.short_description = 'Mark selected products as unavailable'
    
    
@admin.register(BannerModel)
class BannerModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'description']
    search_fields = ['description']
    list_filter = ['description']