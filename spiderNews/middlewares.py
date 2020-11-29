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
# setting 优先级 > 541
class SeleniumNewsDownloaderMiddleware(object):
    # 将driver创建在中间件的初始化方法中，适合项目中只有一个爬虫。
    # 爬虫项目中有多个爬虫文件的话，将driver对象的创建放在每一个爬虫文件中。
    # 在request对象通过中间件的时候，在中间件内部开始使用selenium去请求url，并且会得到url对应的源码，然后再将源代码通过response对象返回，直接交给process_response()进行处理，再交给引擎。过程中相当于后续中间件的process_request()以及Downloader都跳过了。
    def process_request(self, request, spider):
        if spider.name == "spiderBilibiliNews":
            spider.driver.get(request.url)

            time.sleep(0.2)
            origin_code = spider.driver.page_source
            # 将源代码构造成为一个Response对象，并返回。
            res = HtmlResponse(url=request.url, encoding='utf8', body=origin_code, request=request)
            # res = Response(url=request.url, body=bytes(origin_code), request=request)
            return res

    def process_response(self, request, response, spider):
        #print(response.url, response.status)
        return response
