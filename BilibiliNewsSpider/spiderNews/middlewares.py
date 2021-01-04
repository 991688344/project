# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from scrapy.http import HtmlResponse, Response
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class SpidernewsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpidernewsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

####################################  自定义中间件 ################################
# setting 优先级 = 543
class SeleniumNewsDownloaderMiddleware(object):
    # 在request对象通过中间件的时候，在中间件内部开始使用selenium去请求url，并且会得到url对应的源码，然后再将源代码通过response对象返回，直接交给process_response()进行处理，再交给引擎。过程中相当于后续中间件的process_request()以及Downloader都跳过了。
    def process_request(self, request, spider):
        if spider.name == "spiderBilibiliNews":
            spider.driver.get(request.url)
            try:
                if 'global' in request.url:     # 请求的是总页面,判断列表元素是否加载完成
                    WebDriverWait(spider.driver,5).until(
                        EC.presence_of_element_located((By.XPATH,'//ul[@class="vd-list mod-2"]'))    # 判断某个元素是否被加到了 dom 树里，并不代表该元素一定可见
                    )
                else:       # 请求的是具体视频页面,判断标签元素加载完成
                    WebDriverWait(spider.driver,5).until(
                        EC.presence_of_element_located((By.XPATH,'//div[@id="v_tag"]'))    # 判断某个元素是否被加到了 dom 树里，并不代表该元素一定可见
                    )
                origin_code = spider.driver.page_source
                res = HtmlResponse(url=request.url, encoding='utf8', body=origin_code, request=request)     # 将源代码构造成为一个Response对象，并返回。
                return res
            except NoSuchElementException as e:
                print(f"[-] No Such element ,check Network {e}")
                exit(-1)

    def process_response(self, request, response, spider):
        return response
