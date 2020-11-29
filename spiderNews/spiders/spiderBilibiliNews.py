import scrapy


class SpiderbilibilinewsSpider(scrapy.Spider):
    name = 'spiderBilibiliNews'
    allowed_domains = ['https://www.bilibili.com/v/information/global']
    start_urls = ['http://https://www.bilibili.com/v/information/global/']

    def parse(self, response):
        pass
