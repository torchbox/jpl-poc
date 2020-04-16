import base64
import re

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


class DocxImageConverter(ImageConverter):
    src_data_finder = re.compile("base64,(.*)")

    def __call__(self, element, user, **kwargs):
        src_data = self.src_data_finder.search(element['value'])
        if src_data:
            image_content = base64.b64decode(src_data.group(1))
            image_name = "imported-image"
        else:
            image_name, image_content = self.fetch_image(element['value'])
        title = element.get('title', '')
        image = self.import_as_image_model(image_name, image_content, owner=user, title=title)
        return (self.block_name, {'image': image})


class StoryBlockMapper(StreamFieldMapper):
    heading = RichTextConverter('paragraph')
    html = RichTextConverter('paragraph')
    image = DocxImageConverter('image')