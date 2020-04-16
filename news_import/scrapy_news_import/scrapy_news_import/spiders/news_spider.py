import scrapy

NEWS_INDEX = "https://www.jpl.nasa.gov/news/"


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = [
            "news.php?feature=7639",
            "news.php?feature=7640",
            "news.php?feature=7638",
            "news.php?feature=7637",
            "news.php?feature=7636",
            "news.php?feature=7635",
            "news.php?feature=7634",
            "news.php?feature=7633",
            "news.php?feature=7632",
            "news.php?feature=7631",
            "news.php?feature=7629",
            "news.php?feature=7628",
            "news.php?feature=7627",
            "news.php?feature=7626",
            "news.php?feature=7625",
            "news.php?feature=7624",
            "news.php?feature=7623",
            "news.php?feature=7622",
            "news.php?feature=7617",
            "news.php?feature=7620",
            "news.php?feature=7618",
            "news.php?feature=7619",
            "news.php?feature=7616",
            "news.php?feature=7615",
            "news.php?feature=7614",
            "news.php?feature=7613",
            "news.php?feature=7612",
        ]

        for url in urls:
            yield scrapy.Request(
                url=NEWS_INDEX + url, callback=self.parse,
            )

    def parse(self, response):
        yield {
            "title": response.xpath("//meta[@property='og:title']/@content").get(),
            "introduction": response.xpath(
                "//meta[@property='og:description']/@content"
            ).get(),
            "updated_at": response.xpath(
                "//meta[@property='og:updated_time']/@content"
            ).get(),
            "paras": response.xpath("//div[@class='wysiwyg_content']/p").getall(),
            "image": response.xpath("//meta[@name='twitter:image']/@content").get(),
        }
