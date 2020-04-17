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
    )


class IContactAdminGroup(ModelAdminGroup):
    menu_label = 'Mailings'
    menu_order = 500
    menu_icon = "mail"
    items = (MessageAdmin,)


modeladmin_register(IContactAdminGroup)
