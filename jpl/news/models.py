from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images import get_image_model_string
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail_content_import.models import ContentImportMixin

from .blocks import StoryBlock, StoryBlockMapper


class NewsIndex(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["news.NewsPage"]


class NewsPage(ContentImportMixin, Page):
    parent_page_types = ["news.NewsIndex"]

    publication_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Use this field to override the date that the "
        "news item appears to have been published.",
    )
    introduction = models.TextField(
        blank=True,
        help_text="Use this field to give a brief intro to the news article.",
    )
    hero_banner = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        help_text="Image used for the banner and thumbnail on the index page.",
    )
    body = StreamField(StoryBlock())

    mapper_class = StoryBlockMapper

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("introduction"),
        ImageChooserPanel("hero_banner"),
        StreamFieldPanel("body"),
    ]

    api_fields = [
        APIField("introduction"),
        APIField("body"),
        APIField("hero_banner"),
        APIField(
            "hero_thumbnail",
            serializer=ImageRenditionField("fill-400x200", source="hero_banner"),
        ),
    ]
