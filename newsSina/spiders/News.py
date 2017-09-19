# -*- coding: utf-8 -*-
import os
import scrapy


from newsSina.items import NewssinaItem


class NewsSpider(scrapy.Spider):
    name = 'News'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # print(response.body.decode())
        items = []
        # 获取所有大类的ｕｒｌ和标题
        parentUrl = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()
        parentTitle = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()
        # 获取所有小类的标题和ＵＲＬ
        subUrl = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()
        # 抓取所有的大类

        for i in range(0, len(parentTitle)):


            # 设置大类的目录名称
            parentFilename = "./Data/" + parentTitle[i]
            # 判断目录存不存在
            if (not os.path.exists(parentFilename)):
                os.mkdir(parentFilename)
            #   抓取所有的小类

            for j in range(0, len(subUrl)):

                item = NewssinaItem()
            # 保存大类的title 和ｕｒｌ
                item['parentTitle'] = parentTitle[i]
                item['parentUrl'] = parentUrl[i]
                # 判断子类页面的ｕｒｌ和大类的ＵＲＬ是否一致
                if_long = subUrl[j].startswith(item['parentUrl'])
                # 如果一致将存储的目录放在大类目录下
                if(if_long):
                    subFilename = parentFilename + os.sep + subTitle[j]

                    if(not os.path.exists(subFilename)):
                        os.mkdir(subFilename)
                    # 存储小类的ＵＲl 、title 和 filename
                    item['subUrl'] = subUrl[j]

                    item['subTitle'] = subTitle[j]
                    item['subFilename'] = subFilename
                    items.append(item)

        for item in items:
            print(item)
            yield scrapy.Request(url=item['subUrl'], meta={'meta1': item}, callback=self.secode_parse)

    def secode_parse(self, response):

        meta1 = response.meta['meta1']
        print("*********************************************************")
        print(meta1)

        # 取小类中所有的子链接
        sonUrl = response.xpath('//a/@href').extract()
        items = []
        for i in range(0, len(sonUrl)):

            # 检查ｕｒｌ开头是否和大类的ＵＲＬ开头和以.shtml结尾
            if_belong = sonUrl[i].endswith('.shtml') and sonUrl[i].startswith(meta1['parentUrl'])
            # 如果是本大类，则放在ｉｔｅｍ下即可
            if (if_belong):

                item = NewssinaItem()
                item['parentTitle'] = meta1['parentTitle']
                item['parentUrl'] = meta1['parentUrl']
                item['subUrl'] = meta1['subUrl']
                item['subTitle'] = meta1['subTitle']
                item['subFilename'] = meta1['subFilename']
                item['sonUrl'] = sonUrl[i]
                items.append(item)
                # print(item['parentTitle']+"===================================")
        # 发送每个小类中的ｕｒｌ请求，连同ｍｅｔａ数据发送回调函数处理
        for item in items:
                yield scrapy.Request(url=item['sonUrl'], meta={'meta_2': item}, callback=self.detail_parse)

    def detail_parse(self, response):
        """
        数据解析，获取文章的标题和内容
        :param response:
        :return:
        """
        item = response.meta['meta_2']
        content = ""
        head = response.xpath('//h1[@id="artibodyTitle"]/text()').extract()
        # content_list = response.xpath('//div[@id="artibody"]/p/text()').extract()
        content_list = ''.join([k.strip() for k in response.xpath('//div[@id="artibody"]/p/text()').extract()]).replace('\u3000', '')
        for count_one in content_list:
            content += count_one

        item['head'] = head
        item['content'] = content
        yield item