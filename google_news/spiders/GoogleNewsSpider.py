from scrapy import Spider, Request
import re

class GoogleNewsSpider(Spider):
    name = 'google_news'
    def start_requests(self):
        start_url = ['https://news.google.com/?hl=zh-HK&gl=HK&ceid=HK%3Azh-Hant'] # HK news for now
        self.extract = lambda a:re.search('(https?://[^\s]+(?=;))',a).group()
        for url in start_url:
            yield Request(url, callback = self.parse)

    def parse(self, response):
        ARTICLE_SELECTOR = '//article[@data-kind="13"]'
        for article in response.xpath(ARTICLE_SELECTOR):
            TITLE_SELECTOR = './/*[@class="ipQwMb ekueJc RD0gLb"]/a/text()'
            SOURCE_SELECTOR = './/div[@class="SVJrMe"]/a/text()'
            TIME_SELECTOR = './/div[@class="SVJrMe"]/time/@datetime'
            HREF_SELECTOR = './@jslog'
            yield{
                'title':article.xpath(TITLE_SELECTOR).extract_first(),
                'source':article.xpath(SOURCE_SELECTOR).extract_first(),
                'time':article.xpath(TIME_SELECTOR).extract_first(),
                'link':self.extract(article.xpath(HREF_SELECTOR).extract_first())
            }
