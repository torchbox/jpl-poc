from io import BytesIO
import requests
import json

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images.models import Image
from jpl.images.models import CustomImage
from jpl.news.models import NewsIndex, NewsPage


class Command(BaseCommand):
    help = "Imports news from JPL export"

    def add_arguments(self, parser):
        parser.add_argument("url", nargs="+", type=str, help="URL")

    def handle(self, *args, **kwargs):

        news_export_url = kwargs["url"][0]

        # delete existing news pages
        NewsPage.objects.exclude(source__exact="").delete()
        # delete most images
        CustomImage.objects.filter(id__gt=10).delete()

        news_index_page = NewsIndex.objects.all()[0]  # find the first news index page
        # import news pages
        news_items = requests.get(news_export_url).json()
        for news_item in news_items:

            streamfield_paras = []
            for para in news_item["paras"]:
                # print('dirty: ' + para)
                para = (
                    para.replace("<p>", "").replace("</p>", "").replace("<br>", "<br/>")
                )
                # print('dirty: ' + para)
                if len(para):
                    p = {u"type": u"paragraph", u"value": para}
                    streamfield_paras.append(p)

            news_page = NewsPage(
                title=news_item["title"],
                introduction=news_item["introduction"],
                source=news_item["url"],
                publication_date=news_item["updated_at"] + "-0800",
                body=json.dumps(streamfield_paras),
            )

            if news_item["image"]:
                response = requests.get(news_item["image"])
                filename = news_item["image"].split("/")[-1]
                image = CustomImage(
                    title=news_item["title"],
                    file=ImageFile(BytesIO(response.content), name=filename),
                )
                image.save()
                news_page.hero_banner = image
            news_index_page.add_child(instance=news_page)
            news_page.save_revision().publish()
            print("published news page " + news_item["title"])
