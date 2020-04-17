import re

from bs4 import BeautifulSoup
from django import forms
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import mark_safe, strip_tags
from django.utils.text import slugify
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core.rich_text import RichText
from wagtail.core.signals import page_published
from wagtail.images import get_image_model_string
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from dateutil.parser import parse
from dateutil.parser._parser import ParserError

from jpl.icontact.models import Message
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


class RelatedLink(Orderable, models.Model):
    parent = ParentalKey(
        "news.NewsPage", on_delete=models.CASCADE, related_name="related_links"
    )
    related_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        PageChooserPanel("related_page", "news.NewsPage"),
    ]


class NewsIndex(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["news.NewsPage"]

    def get_context(self, request):
        context = super().get_context(request)

        context["posts"] = (
            NewsPage.objects.descendant_of(self).live().order_by("-publication_date")
        )

        return context


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

    source = models.TextField(
        blank=True, help_text="Where was this content imported from?",
    )
    publish_to_icontact = models.BooleanField(
        default=False,
        help_text="If checked, a draft message will be created on iContact the next time this page is published",
    )

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

    promote_panels = Page.promote_panels + [
        InlinePanel("related_links", label="Related links", max_num=3)
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("source"),
        FieldPanel("publish_to_icontact"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(taxonomy_panels, heading="Taxonomy"),
            ObjectList(promote_panels, heading="Promote"),
            ObjectList(settings_panels, heading="Settings", classname="settings"),
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

    @classmethod
    def create_from_import(cls, parsed_doc, user):
        """
        Factory method to create the Page and populate it from a parsed document.
        """

        date = None
        title = None
        introduction = None
        mapper_class = cls.mapper_class
        mapper = mapper_class()
        imported_data = mapper.map(parsed_doc['elements'], user=user)

        date_matching_pattern = re.compile(r"""
        [a-z]+  # at least one ascii letter (month)
        \s      # one space after
        \d\d?   # one or two digits (day)
        (?:th)?   # optional 'th'
        ,?      # an optional comma
        \s      # one space after
        \d{4}   # four digits (year)
        """, re.IGNORECASE | re.VERBOSE)

        bold_title_matching_pattern = re.compile(r"<b>(.*[a-z].*)</b>", re.IGNORECASE)

        streamfield_data = []
        for block_name, value in imported_data:
            if not title:
                # Don't import anything before the title (first bit of bold text) into the streamfield proper
                if not date:
                    # If there's a date before the title, import the first one as the publication date

                    results = date_matching_pattern.findall(str(value))
                    for match in results:
                        try:
                            date = parse(match)
                            break
                        except ParserError:
                            pass
                bold_text = bold_title_matching_pattern.search(str(value))
                if bold_text:
                    # If the title is coming from RichText, it has already been cleaned of all non-Draftail compatible tags
                    title = mark_safe(strip_tags(bold_text.group())) if isinstance(value, RichText) else strip_tags(bold_text.group())
                continue
            elif "-end-" in str(value):
                # Don't import anything after "-end-"
                break
            elif not introduction:
                # Don't import anything before the intro
                # If the intro is coming from RichText, it has already been cleaned of all non-Draftail compatible tags
                introduction = mark_safe(strip_tags(value)) if isinstance(value, RichText) else strip_tags(value)
            else:
                streamfield_data.append((block_name, value))

        return cls(
            title=title,
            introduction=introduction,
            slug=slugify(title),
            body=streamfield_data,
            owner=user,
            publication_date=date,
        )


def publish_to_icontact(sender, instance, **kwargs):
    if instance.publish_to_icontact:
        # Reset flag
        instance.publish_to_icontact = False
        instance.save()

        context = {'page': instance}
        html_body = render_to_string('news/news_page_icontact.html', context)
        soup = BeautifulSoup(render_to_string('news/news_page_icontact.txt', context))
        text_body = '\n'.join(line.strip() for line in soup.get_text().splitlines())

        # Create message
        # Creating the message will also create it on iContact
        Message.objects.create(
            campaign_id=settings.ICONTACT_SETTINGS["campaign_id"],
            message_name=f"{sender.__name__}: {instance.pk}",
            subject=instance.title,
            html_body=html_body,
            text_body=text_body,
            source_page=instance,
        )


page_published.connect(publish_to_icontact, sender=NewsPage)
