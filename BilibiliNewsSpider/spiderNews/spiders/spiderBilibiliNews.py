import scrapy
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from spiderNews.items import SpidernewsItem
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import platform


class SpiderbilibilinewsSpider(scrapy.Spider):
    name = 'spiderBilibiliNews'
    allowed_domains = ['https://www.bilibili.com/v/information/global']
    start_urls = []
    count = 0       # 爬取过的总页数
    maxPage = 100   # 默认最大爬取的页数
    def __init__(self):
	# 在初始化爬取对象时，创建driver 供中间件使用
        super(SpiderbilibilinewsSpider, self).__init__(name='spiderBilibiliNews')
        chrome_options = webdriver.ChromeOptions()  # 模拟谷歌浏览器
        prefs = {"profile.managed_default_content_settings.images":2} # 不加载图片
        chrome_options.add_experimental_option("prefs",prefs)
        chrome_options.add_argument('--headless')     # 无头浏览
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])   # 不输出日志
        chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错

        if(platform.system() == 'Windows'):
            self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='./Pluggins/chromedriver.exe')
        elif (platform.system() == 'Linux'):
            self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='./Pluggins/chromedriver')

        # 视频热度排序的URL随时间变化,所以从初始页面动态获取
        r = requests.get('https://www.bilibili.com/v/information/global')
        html = etree.HTML(r.text)
        url = html.xpath('//div[@class="left"]//a/@href')[1]  # 获取视频热度排序url
        self.start_urls.append('https://www.bilibili.com/v/information/global/'+url)
        try:
            self.maxPage = int(input("[?] 最大爬取几页(默认爬取全部40多页): "))
        except:
                print("[-] 使用默认参数")
                self.maxPage = 100

    def parse(self, response):
        self.count = self.count + 1
        if self.count > self.maxPage:
            return None
        print(f"{'*'*40}第{self.count}页{'*'*40}")
        print(f"[*] Page URL :{response.url}")
        link = response.xpath('//div[@class="r"]/a/@href').extract()    # 视频真实地址
        # 爬取这个页面上所有视频
        for i in link:
            realURL = "https://"+i[2:]
            print(f"[*] realURL {realURL}")
            yield scrapy.Request(realURL,callback=self.getTag_parse,dont_filter=True)

        # 如果有下一页继续爬取下一页
        try:
            #print(f"[*] Start URL : {self.start_urls}")
            self.driver.get(self.start_urls.pop())  # start_urls 存储当前访问的主页面,用来供找到下一页使用
            self.driver.find_elements_by_xpath('//li[@class="page-item next"]')[0].click()
            nextURL = self.driver.current_url
            self.start_urls.append(nextURL)
            #print(f"[*] Next Page URL :{nextURL}")
            yield scrapy.Request(nextURL,callback=self.parse,dont_filter=True)
        except Exception as e:
            print(f"[-] next Page NotFound: {e}")

    def getTag_parse(self,response):
        #print("[*] 进入回调函数")
        item = SpidernewsItem()
        tags = response.xpath('//li[@class="tag"]/div/a/span/text()').extract()
        tags = tags + response.xpath('//li[@class="tag"]/a/span/text()').extract()
        tags = tags + [i.strip() for i in response.xpath('//li[@class="tag"]/div/a/text()').extract()]
        item['tag'] = tags
        #print(f"[*] {tags}")
        yield item

    # 结束后关闭浏览器
    def close(self,spider):
        self.driver.quit()
