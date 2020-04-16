from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import NewsCategory


class NewsCategoryAdmin(ModelAdmin):
    model = NewsCategory
    menu_icon = 'list-ul'
    menu_order = 400
    list_display = ("name",)


modeladmin_register(NewsCategoryAdmin)
