import requests
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.models import Page, Orderable
from wagtail.search import index
from django.core.cache import cache
from wagtail.snippets.models import register_snippet

from pose.settings.base import CATALOG_HOST, CATALOG_API_KEY

CATALOG_CACHE_TTL = 60 * 10  # 10 minutes


class HomePage(Page):

    # Hero section
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage hero image",
    )
    hero_text = models.CharField(blank=True, max_length=255, help_text="Tagline")
    hero_description = models.CharField(
        blank=True, max_length=255, help_text="Introductory sentence"
    )
    hero_cta = models.CharField(
        blank=True,
        verbose_name="Primary CTA",
        max_length=255,
        help_text="Primary Call to Action text",
    )
    hero_cta_link = models.URLField(
        blank=True,
    )
    secondary_action_label = models.CharField(
        blank=True,
        verbose_name="Secondary Action Label",
        max_length=255,
        help_text="Secondary Action label",
    )
    secondary_action_link = models.URLField(
        blank=True,
    )

    # Community section
    community_title = models.CharField(
        blank=True,
        verbose_name="Community Section Title",
        max_length=255,
    )

    community_body = RichTextField(blank=True)
    community_cta = models.CharField(
        blank=True,
        verbose_name="Community CTA",
        max_length=255,
    )
    community_cta_link = models.URLField(
        blank=True,
    )
    community_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Community illustration",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Catalog section
    catalog_title = models.CharField(
        blank=True,
        verbose_name="Catalog Section Title",
        max_length=255,
    )
    catalog_body = RichTextField(blank=True)
    catalog_cta = models.CharField(
        blank=True,
        verbose_name="Catalog CTA",
        max_length=255,
    )
    catalog_cta_link = models.URLField(
        blank=True,
    )
    catalog_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Catalog illustration",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Dynamic

    @property
    def catalog_extension_count(self):
        """Returns the number of CKAN extensions cataloged."""

        # check cache
        cached = cache.get("catalog_counts")

        if cached:
            return cached
        extensions = 0
        sites = 0
        try:
            # request counts from catalog
            extensions = requests.get(
                f"{CATALOG_HOST}/api/3/action/package_search?fq=type:extension&rows=0",
            ).json()["result"]["count"]

            sites = requests.get(
                f"{CATALOG_HOST}/api/3/action/package_search?fq=type:site&rows=0",
            ).json()["result"]["count"]

            cache.set(
                "catalog_counts",
                {
                    "extensions": extensions,
                    "sites": sites,
                },
                CATALOG_CACHE_TTL,
            )
        finally:

            return {
                "extensions": extensions,
                "sites": sites,
            }

    # content panels
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_text"),
                FieldPanel("hero_description"),
                FieldPanel("hero_cta"),
                FieldPanel("hero_cta_link"),
                FieldPanel("secondary_action_label"),
                FieldPanel("secondary_action_link"),
            ],
            heading="Hero section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("community_title"),
                FieldPanel("community_body"),
                FieldPanel("community_cta"),
                FieldPanel("community_cta_link"),
                FieldPanel("community_image"),
            ],
            heading="Community section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("catalog_title"),
                FieldPanel("catalog_body"),
                FieldPanel("catalog_cta"),
                FieldPanel("catalog_cta_link"),
                FieldPanel("catalog_image"),
            ],
            heading="Catalog section",
        ),
    ]


class MainNavItem(models.Model):
    label = models.CharField()
    url = models.URLField(
        verbose_name="External URL",
        null=True,
        blank=True,
        help_text="Will override Internal Page if provided.",
    )

    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Internal Page",
        help_text="Will be overridden by External URL if one is provided",
    )

    order = models.PositiveIntegerField(
        default=0, help_text="Used to determine order when rendering"
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("url"),
        FieldPanel("page"),
        FieldPanel(
            "order",
        ),
    ]

    def __str__(self):
        return self.label
