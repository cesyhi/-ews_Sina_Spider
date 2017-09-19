# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewssinaItem(scrapy.Item):

    # 页面大类的标题和ｕｒｌ
    parentTitle = scrapy.Field()
    parentUrl = scrapy.Field()
    # 页面小类的标题和ＵＲＬ
    subTitle = scrapy.Field()
    subUrl = scrapy.Field()
    # 小类的存储路径
    subFilename = scrapy.Field()
    # 小类中的子类的ＵＲＬ
    sonUrl = scrapy.Field()
    # 文章的标题和内容
    head = scrapy.Field()
    content= scrapy.Field()