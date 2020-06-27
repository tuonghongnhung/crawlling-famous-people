# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlingpeopleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    quick_info = scrapy.Field()
    detail_info = scrapy.Field()
    link = scrapy.Field()

class ImageItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    
