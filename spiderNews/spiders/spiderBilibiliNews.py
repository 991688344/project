import scrapy
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

class SpiderbilibilinewsSpider(scrapy.Spider):
    name = 'spiderBilibiliNews'
    allowed_domains = ['https://www.bilibili.com/v/information/global']
    start_urls = []

    def __init__(self):
	# 在初始化爬取对象时，创建driver 供中间件使用
        super(SpiderbilibilinewsSpider, self).__init__(name='spiderBilibiliNews')
        option = FirefoxOptions()	#模拟火狐浏览器
        option.headless = True
        self.driver = webdriver.Firefox(options=option,executable_path='./Pluggins/geckodriver.exe')
        # 视频热度排序的URL随时间变化,所以从初始页面动态获取
        r = requests.get('https://www.bilibili.com/v/information/global')
        html = etree.HTML(r.text)
        url = html.xpath('//div[@class="left"]//a/@href')[1]  # 获取视频热度排序url
        self.start_urls.append('https://www.bilibili.com/v/information/global/'+url)

    def parse(self, response):
        link = response.xpath('//div[@class="r"]')
        print(f"[*] spider Link: {link}")

        #count = 0
        #for i in link:
        #    realURL = "https://"+i[2:]
        #    print(f"[*] realURL {realURL}")
        #    yield scrapy.Request(realURL,callback=self.getTag_parse,dont_filter=True)


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

    # 结束后关闭浏览器
    def close(self,spider):
        self.driver.quit()
