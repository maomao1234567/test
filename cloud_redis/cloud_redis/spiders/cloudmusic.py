# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import CloudRedisItem


class CloudmusicSpider(CrawlSpider):
    name = 'cloudmusic'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/#/discover/artist']

    rules = (
        Rule(LinkExtractor(allow=r'/discover/artist', restrict_xpaths='//div[@class="blk"]/ul/li'), follow=True),
        Rule(LinkExtractor(allow=r'/discover/artist', restrict_xpaths='//div[@class="g-wrap"]/ul/li'), follow=True),
        Rule(LinkExtractor(allow=r'/artist?id', restrict_xpaths='//div[@class="m-sgerlist"]/ul/li'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = CloudRedisItem()

        return item
