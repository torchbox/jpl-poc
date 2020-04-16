from wagtail.embeds.finders.base import EmbedFinder


class NASAEyes(EmbedFinder):

    def accept(self, url):
        return url.startswith("https://eyes.nasa.gov/apps/orrery")

    def find_embed(self, url, max_width=None):
        html = f'<iframe class="test" width="98%" height="300" src="{url}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

        # 16:9 aspect ratio
        return {
            "title": "NASA's Eyes",
            "author_name": "NASA",
            "provider_name": "NASA's Eyes",
            "type": "rich",
            "thumbnail_url": "",
            "width": 800,
            "height": 450,
            "html": html,
        }
