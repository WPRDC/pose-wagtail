from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from home.models import MainNavItem


class MainNavViewSet(SnippetViewSet):
    model = MainNavItem

    panels = [
        FieldPanel("label"),
        FieldPanel("url"),
        FieldPanel("page"),
        FieldPanel("order"),
    ]


register_snippet(MainNavViewSet)
