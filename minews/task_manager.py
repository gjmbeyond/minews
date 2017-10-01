#coding=utf8

from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from minews.spiders.ithome_spider import IthomeSpider
import logging
from minews.settings import LOG_LEVEL
logging.basicConfig(level=LOG_LEVEL)

class IthomeSpiderProcess(Process):

    def __init__(self, *argus, **keywords):
        Process.__init__(self)
        self.argus = argus
        self.keywords = keywords
    
    def run(self):
        logging.debug('process start')
        process = CrawlerProcess()
        process.crawl(IthomeSpider)
        process.start() # the script will block here until all crawling jobs are finished

if '__main__' == __name__:
    process = IthomeSpiderProcess()
    process.start()
