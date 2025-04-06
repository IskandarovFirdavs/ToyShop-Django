from django import template

register = template.Library()

@register.simple_tag
def get_heart_icon(request, product):
    return "fas fa-heart" if request.user in product.wishlist.all() else "far fa-heart"


