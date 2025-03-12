from django import template
from home.models import MainNavItem

register = template.Library()


@register.inclusion_tag("home/tags/main_nav_items.html", takes_context=True)
def main_nav_items(context):
    return {
        "items": MainNavItem.objects.all().order_by("order"),
        "request": context["request"],
    }
