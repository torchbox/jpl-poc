from django.utils.html import mark_safe
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import Message


class MessageAdmin(ModelAdmin):
    model = Message
    menu_icon = "list-ul"
    list_display = (
        "message_name",
        "subject",
        "icontact_message_url",
        "created_at",
        "updated_at",
    )

    def icontact_message_url(self, obj):
        if obj.icontact_message_id:
            return mark_safe(
                f'<a href="https://app.icontact.com/icp/core/fusion/messages/{obj.icontact_message_id}" target="_blank">'
                f"Message ID: {obj.icontact_message_id}"
                "</a>"
            )

        return ""

    icontact_message_url.short_description = "View on iContact"


class IContactAdminGroup(ModelAdminGroup):
    menu_label = "Mailings"
    menu_order = 500
    menu_icon = "mail"
    items = (MessageAdmin,)


modeladmin_register(IContactAdminGroup)
