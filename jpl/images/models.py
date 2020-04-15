from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition, Image


class CustomImage(AbstractImage):
    caption = models.TextField(blank=True)
    alt = models.CharField("Alt text", max_length=255, blank=True)
    credit = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + ("caption", "alt", "credit",)

    def save(self, *args, **kwargs):
        # If not specified, the title becomes the alt text
        if not self.alt:
            self.alt = self.title

        super().save(*args, **kwargs)


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        "images.CustomImage", related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
