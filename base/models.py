from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PublishingPanel,
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.fields import RichTextField
from wagtail.models import (
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
)

from wagtail.snippets.models import register_snippet


@register_setting
class GlobalSettings(BaseGenericSetting):

    ckan_logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="CKAN logo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="CKAN logo image",
    )

    ckan_url = models.URLField(verbose_name="CKAN URL", null=True, blank=True)

    dathere_logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="DatHere logo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="DatHere logo image",
    )

    dathere_url = models.URLField(verbose_name="DatHere URL", null=True, blank=True)

    pitt_logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Pitt logo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Pitt logo image",
    )
    pitt_url = models.URLField(verbose_name="Pitt URL", null=True, blank=True)

    wprdc_logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="WPRDC logo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="WPRDC logo image",
    )
    wprdc_url = models.URLField(verbose_name="WPRDC URL", null=True, blank=True)

    github_url = models.URLField(verbose_name="GitHub URL", blank=True)

    nsf_logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="NSF logo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="NSF logo image",
    )
    nsf_url = models.URLField(verbose_name="NSF URL", null=True, blank=True)

    funding_text = RichTextField(blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("ckan_logo"),
                FieldPanel("ckan_url"),
                FieldPanel("dathere_logo"),
                FieldPanel("dathere_url"),
                FieldPanel("pitt_logo"),
                FieldPanel("pitt_url"),
                FieldPanel("wprdc_logo"),
                FieldPanel("wprdc_url"),
                FieldPanel("nsf_logo"),
                FieldPanel("nsf_url"),
            ],
            "Logos",
        ),
        MultiFieldPanel(
            [
                FieldPanel("funding_text"),
            ],
            "Footer content",
        ),
        MultiFieldPanel(
            [
                FieldPanel("github_url"),
            ],
            "Social settings",
        ),
    ]


@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"


@register_snippet
class HighlightedExtension(models.Model):
    slug = models.CharField(max_length=255, verbose_name="Extension ID")

    panels = [
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.slug


@register_snippet
class HighlightedSite(models.Model):
    slug = models.CharField(max_length=255, verbose_name="Site ID")

    panels = [
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.slug
