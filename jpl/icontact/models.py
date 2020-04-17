from django.db import models
from django.contrib.postgres.fields import JSONField
from wagtail.admin.edit_handlers import FieldPanel

from jpl.icontact.api import IContactAPI


class Message(models.Model):
    campaign_id = models.PositiveIntegerField()
    message_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=255)
    html_body = models.TextField()
    text_body = models.TextField()

    source_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    icontact_message = JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("campaign_id"),
        FieldPanel("message_name"),
        FieldPanel("subject"),
        FieldPanel("html_body"),
        FieldPanel("text_body"),
    ]

    def __str__(self):
        return self.message_name

    @property
    def icontact_message_id(self):
        return self.icontact_message.get("messageId")

    def save(self, *args, create_message=True, **kwargs):

        if create_message:
            api = IContactAPI()
            resp = api.create_message(
                message_name=self.message_name,
                subject=self.subject,
                html_body=self.html_body,
                text_body=self.text_body,
            )

            self.icontact_message = resp.json()["messages"][0]

        super().save(*args, **kwargs)
