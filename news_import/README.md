## Import JPL news items

1. Scrape the JPL news site:

```
cd scrapy_news_import
scrapy crawl news -o news.json
```

2. Put the contents of `news.json` somewhere public, e.g. https://gist.github.com/tomdyson/097135356e6c748499ee3de68b560691

3. Import into Wagtail

`./manage.py importnews https://gist.githubusercontent.com/tomdyson/097135356e6c748499ee3de68b560691/raw/af1ede5f00426bfd5626ef20c80ef1acf6e995be/jpl-news.json`