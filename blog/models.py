from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class BlogIndexPage(Page):

    subtitle = models.CharField(
        null=True,
        blank=True,
        max_length=255,
    )
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        "subtitle",
        "intro",
    ]

    def get_context(self, request, **kwargs):
        context = super().get_context(request)
        # limit to published blog posts only and propertly order
        blogpages = (
            self.get_children().live().type(BlogPage).order_by("-first_published_at")
        )
        context["blogpages"] = blogpages
        return context


class BlogTagIndexPage(Page):

    def get_context(self, request, **kwargs):

        # Filter by tag
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogPage(Page):

    authors = ParentalManyToManyField("blog.Author", blank=True)
    body = RichTextField()
    date = models.DateField("Post date")

    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    intro = RichTextField(
        blank=True, help_text="A brief introduction shown only in lists and previews."
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    tagline = models.CharField(
        null=True,
        blank=True,
        max_length=127,
    )

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.SearchField("tagline"),
        index.FilterField("date"),
    ]

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("authors"),
        FieldPanel("tags"),
        FieldPanel("intro"),
        MultiFieldPanel(
            [
                "tagline",
                "body",
            ],
            heading="Content",
        ),
        InlinePanel(
            "related_links",
            heading="Related links",
            label="Related link",
        ),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel("feed_image"),
    ]

    # Parent page / subpage type rules
    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = ["image", "caption"]


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="related_links")
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
    ]


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = ["name", "author_image"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"
