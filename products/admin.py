from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import CategoryModel, ColorModel, ProductModel, BannerModel, CommentModel
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


@admin.register(ProductModel)
class ProductModelAdmin(MyTranslationAdmin):
    list_display = ['id', 'name', 'price', 'category', 'color', 'is_available']
    search_fields = ['name', 'category__name', 'color__name']
    list_filter = ['category', 'color', 'is_available']
    autocomplete_fields = ['category', 'color']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    ordering = ['id']

    fieldsets = (
        (None, {
            'fields': (
                'name', 'price', 'short_description', 'long_description', 
                'discount', 'image', 'extra_images', 'is_available', 
                'availability', 'quantity', 'category', 'color', 'age_range', 'sku'
            )
        }),
    )

    actions = ['make_available', 'make_unavailable']

    @admin.action(description=_("Tanlangan mahsulotlarni mavjud deb belgilash"))
    def make_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description=_("Tanlangan mahsulotlarni mavjud emas deb belgilash"))
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)


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
