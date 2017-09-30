import scrapy
from scrapy.spider import Spider

class BaiduTestSpider(Spider):
    name = 'BaiduTestSpider'

    def __init__(self, param1=None, *args, **kwargs):
        super(BaiduTestSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.baidu.com/']
    
    def start_requests(self):
        yield scrapy.FormRequest(self.start_urls[0], callback=self.parse_content)

    def parse_content(self, response):
        print "enter %s" % self.parse_content.__name__
        print response.body
