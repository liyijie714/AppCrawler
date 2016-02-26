from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from nettuts.items import NettutsItem
from scrapy.http import Request
import re
import scrapy

class MySpider(BaseSpider):
    name = "huawei"
    allowed_domains = ["huawei.com"]
    start_urls = ["http://appstore.huawei.com/more/all"]
    def parse(self, response):
        page = Selector(response)
        hrefs = page.xpath('//h4[@class="title"]/a/@href')

        for href in hrefs:
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        page = Selector(response)
        item = NettutsItem()
        item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
        item['url'] = response.url
        item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)
        item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')
        item['thumbnail'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/img[@class="app-ico"]/@lazyload').extract()
        divs = page.xpath('//div[@class="open-info"]')
        recom = ""

        for div in divs:
            url = div.xpath('./p[@class="name"]/a/@href').extract_first()
            recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
            name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
            recom += "{0}:{1}.".format(recommended_appid, name)
        item['recommended'] = recom
            # print "==================="
            # print "??: ",item['title']
            # print "==================="
        yield item

        # print "------------------------"
        # print "??: ",divs
        # print "------------------------"
        