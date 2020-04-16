from django import forms
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images import get_image_model_string
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from wagtail_content_import.models import ContentImportMixin

from .blocks import StoryBlock, StoryBlockMapper


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey("news.NewsPage", related_name="news_tags")


class NewsCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [FieldPanel("name"), FieldPanel("slug")]

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class NewsIndex(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["news.NewsPage"]


class NewsPage(ContentImportMixin, Page):
    parent_page_types = ["news.NewsIndex"]
    subpage_types = []

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

    categories = ParentalManyToManyField("news.NewsCategory", blank=True)
    tags = ClusterTaggableManager(through="news.NewsPageTag", blank=True)

    mapper_class = StoryBlockMapper

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("introduction"),
        ImageChooserPanel("hero_banner"),
        StreamFieldPanel("body"),
    ]

    taxonomy_panels = [
        MultiFieldPanel(
            [FieldPanel("categories", widget=forms.CheckboxSelectMultiple)],
            heading="Categories",
        ),
        FieldPanel("tags"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(taxonomy_panels, heading="Taxonomy"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    api_fields = [
        APIField("publication_date"),
        APIField("introduction"),
        APIField("body"),
        APIField("hero_banner"),
        APIField(
            "hero_thumbnail",
            serializer=ImageRenditionField("fill-400x200", source="hero_banner"),
        ),
    ]
