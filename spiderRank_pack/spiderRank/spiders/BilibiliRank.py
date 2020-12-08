import scrapy
from spiderRank.items import SpiderrankItem


class BilibilirankSpider(scrapy.Spider):
    name = 'BilibiliRank'
    allowed_domains = ['https://www.bilibili.com/v/popular/rank/all']
    start_urls = ['https://www.bilibili.com/v/popular/rank/all/']
    def parse(self, response):
        title = response.xpath('//li[@class="rank-item"]//div[@class="info"]/a/text()').extract()
        print(title)
        link = response.xpath('//li[@class="rank-item"]//div[@class="info"]/a/@href').extract()
        print(link)
        print(len(link))
        count = 0
        for i in link:
            realURL = "https://"+i[2:]
            print(f"[*] realURL {realURL}")
            yield scrapy.Request(realURL,callback=self.getTag_parse,dont_filter=True)


    def getTag_parse(self,response):
        print("[*] 进入回调函数")
        realURL = response.url
        item = SpiderrankItem()
        tags = response.xpath('//li[@class="tag"]/div/a/span/text()').extract()
        tags = tags + response.xpath('//li[@class="tag"]/a/span/text()').extract()
        tags = tags + [i.strip() for i in response.xpath('//li[@class="tag"]/div/a/text()').extract()]
        item['tag'] = tags
        #print(f"[*] {tags}")
        yield item
