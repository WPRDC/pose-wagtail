import requests
from django import template
from django.core.cache import cache

from base.models import HighlightedExtension, HighlightedSite
from pose.settings.base import CATALOG_HOST

register = template.Library()


def get_details(slug: str, widget_type: str) -> dict:
    cache_key = f"widgets/{slug}"
    result = None

    # on cache miss
    if result is None:
        result: dict = requests.get(
            f"{CATALOG_HOST}/api/3/action/package_show?id={slug}",
        ).json()["result"]

        last_update = result.get("last_update")
        if last_update:
            from datetime import datetime

            result["last_update"] = datetime.strptime(last_update, "%m/%d/%Y")
            result["catalog_link"] = f"{CATALOG_HOST}/{widget_type}/{slug}"
        cache.set(cache_key, result)
    return result


def _get_widgets(model: type[HighlightedSite | HighlightedExtension]) -> dict:
    """Get details for highlighted widgets for a class."""
    object_ids = [obj.slug for obj in model.objects.all()]

    widget_type = ""

    if model == HighlightedSite:
        widget_type = "site"
    elif model == HighlightedExtension:
        widget_type = "extension"

    objs = []
    for obj_id in object_ids:
        objs.append(
            get_details(
                obj_id,
                widget_type,
            ),
        )

    return {
        "widgets": objs,
    }


@register.inclusion_tag("base/includes/ckan_widgets.html")
def get_highlighted_extensions_widget():
    return _get_widgets(HighlightedExtension)


@register.inclusion_tag("base/includes/ckan_widgets.html")
def get_highlighted_sites_widget():
    return _get_widgets(HighlightedSite)
