from datetime import datetime

import requests
from django import template
from django.core.cache import cache
from rich import emoji

from base.models import HighlightedExtension, HighlightedSite, HighlightedDiscussion
from pose.settings.base import CATALOG_HOST

register = template.Library()


def get_details(slug: str, widget_type: str) -> dict:
    """Get details for highlighted widgets for a class."""
    cache_key = f"widgets/{slug}"
    result = cache.get(cache_key)

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
        cache.set(cache_key, result, 60 * 60 * 24)
    return result


def _get_widgets(model: type[HighlightedSite | HighlightedExtension]) -> dict:
    object_ids = [obj.slug for obj in model.objects.all()]

    widget_type = ""

    if model == HighlightedSite:
        widget_type = "site"
    elif model == HighlightedExtension:
        widget_type = "extension"

    objs = []
    for obj_id in object_ids:
        try:
            objs.append(
                get_details(
                    obj_id,
                    widget_type,
                ),
            )
        except Exception:
            pass

    return {
        "widgets": objs,
    }


@register.inclusion_tag("base/includes/ckan_widgets.html")
def get_highlighted_extensions_widget():
    return _get_widgets(HighlightedExtension)


@register.inclusion_tag("base/includes/ckan_widgets.html")
def get_highlighted_sites_widget():
    return _get_widgets(HighlightedSite)


@register.inclusion_tag("base/includes/discourse_widgets.html")
def get_highlighted_discussions_widget():
    """
    Collects data on curated topics for use in widgets.

    Discourse docs: https://docs.discourse.org/#tag/Topics/operation/getTopic
    """
    topics = cache.get("highlighted_topics", [])

    if topics:
        return {
            "topics": topics,
        }

    try:
        for topic_id in [t.topic_id for t in HighlightedDiscussion.objects.all()]:
            topics.append(
                requests.get(
                    f"https://community.civicdataecosystem.org/t/{topic_id}.json"
                ).json()
            )
        cache.set("highlighted_topics", topics)
    finally:
        return {
            "topics": topics,
        }


@register.inclusion_tag("base/includes/discourse_widgets.html")
def get_top_discussions_widget():
    """
    Collects data on the past month's trending topics for use in widgets.

    Discourse docs: https://docs.discourse.org/#tag/Topics/operation/listTopTopics
    """
    topics = cache.get("top_topics", [])
    if topics:
        return {
            "topics": topics,
        }
    try:
        topics = requests.get(
            f"https://community.civicdataecosystem.org/top.json",
            params={"period": "yearly", "per_page": 5},
        ).json()["topic_list"]["topics"]
        topics = [
            {
                **t,
                "last_updated": datetime.fromisoformat(t["last_posted_at"]),
                "title": emoji.Emoji.replace(t["fancy_title"] or t["title"]),
                "excerpt": emoji.Emoji.replace(t["excerpt"]),
            }
            for t in topics
        ]
        cache.set("top_topics", topics)
    finally:
        return {
            "topics": topics,
        }
