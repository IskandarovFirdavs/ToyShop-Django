from modeltranslation.translator import register, TranslationOptions
from .models import CategoryModel, ColorModel, ProductModel, BannerModel

@register(CategoryModel)
class CategoryModelTranslationOptions(TranslationOptions):
    fields = ('name',)  

@register(ColorModel)
class ColorModelTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(ProductModel)
class ProductModelTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'long_description',)
    

@register(BannerModel)
class BannerModelTranslationOptions(TranslationOptions):
    fields = ('description',)
    
