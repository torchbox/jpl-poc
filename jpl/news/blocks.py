from django.core.exceptions import ValidationError
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock as DefaultEmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from wagtail_content_import.mappers.converters import ImageConverter, RichTextConverter
from wagtail_content_import.mappers.streamfield import StreamFieldMapper


class EmbedBlock(blocks.StructBlock):
    embed = DefaultEmbedBlock()
    caption = blocks.TextBlock(required=False)
    credit = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        icon = "media"
        template = "blocks/embed_block.html"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class StoryBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "link"])
    image = ImageBlock()
    embed = EmbedBlock()


class StoryBlockMapper(StreamFieldMapper):
    heading = RichTextConverter('paragraph')
    html = RichTextConverter('paragraph')
    image = ImageConverter('image')
    