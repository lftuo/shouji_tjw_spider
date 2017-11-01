#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2017-11-1 09:26:29
# @File : ShoujiTjwSpider.py
# @Software : IntelliJ IDEA
# 爬取天极网产品库
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from shouji_tjw_spider.items import ShoujiTjwSpiderItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class shouji_tjw_spider(scrapy.Spider):
    # 命名爬虫名称
    name = "tjw_spider"
    allowed_domins = ["product.yesky.com"]
    # 设置爬虫URL
    start_urls = []
    for i in range(215):
        url = "http://product.yesky.com/mobilephone/list%s.html"%(i+1)
        #print url
        start_urls.append(url)

    '''
    重写解析函数
    :param response:自动获取URL返回response
    '''
    def parse(self, response):
        phones = response.xpath(".//div[@id='prolist']/div[@class='list blue']")
        for phone in phones:
            # 获取详细参数链接
            url = phone.xpath("./p/a/@href").extract()[0]+"param.shtml"
            print url
            #item = ShoujiTjwSpiderItem(url)
            request = scrapy.Request(url=url, callback=self.parse_param_url)
            #request.meta['item'] = item
            yield request

    def parse_param_url(self,response):
        #item = response.meta['item']
        basic_params = response.xpath(".//table[@id='pro_links1']/following-sibling::*")[0].xpath("./tr/following-sibling::*")[0].xpath("string(./th)").extract()[0]
        #print basic_params.strip()
        if basic_params.strip() == '手机昵称'.encode('utf-8'):
            model = response.xpath(".//table[@id='pro_links1']/following-sibling::*")[0].xpath("./tr/following-sibling::*")[0].xpath("./th/following-sibling::*")[0].xpath("./text()").extract()[0]
            print model.strip()


if __name__ == '__main__':
    # 启动tjw_spider爬虫
    process = CrawlerProcess(get_project_settings())
    process.crawl('tjw_spider')
    process.start()