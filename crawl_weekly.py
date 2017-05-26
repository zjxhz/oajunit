# import scrapy
# from scrapy.crawler import CrawlerProcess
#
# from oajunit.spiders.tests import TestsSpider
#
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
#
# process.crawl(TestsSpider)
# process.start()

from scrapy import cmdline

cmdline.execute("scrapy crawl tests -o tests_weekly.json".split())