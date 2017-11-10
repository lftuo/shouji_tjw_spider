#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2017-11-1 09:26:29
# @File : ShoujiTjwSpider.py
# @Software : IntelliJ IDEA
# 爬取天极网产品库
import logging

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
        start_urls.append(url)

    def parse(self, response):
        '''
        重写解析函数
        :param response: 自动获取URL返回response
        :return:
        '''

        phones = response.xpath(".//div[@class='list blue']")
        for phone in phones:
            # 获取详细参数链接
            url = phone.xpath("./p/a/@href").extract()[0]+"param.shtml"
            #url = "http://product.yesky.com/product/1007/1007472/param.shtml"
            id = url.split("/")[len(url.split("/"))-3]+"-"+url.split("/")[len(url.split("/"))-2]
            title = ""
            price = ""
            screen_size = ""
            resolution = ""
            try:
                # 解析标题
                title = phone.xpath("./h2/a/text()").extract()[0]
                # 解析价格
                price = phone.xpath("./span/h3/a/text()").extract()[0].replace('￥','').strip()
                # 解析屏幕尺寸
                screen_size = phone.xpath("./ul/li")[0].xpath("./text()").extract()[0].replace('屏幕尺寸：','').strip()
                # 解析分辨率
                resolution = phone.xpath("./ul/li")[1].xpath("./text()").extract()[0].replace('分辨率：','').strip()
            except Exception,e:
                logging.exception(e)

            item = ShoujiTjwSpiderItem(id=id,url=url,title=title,price=price,screen_size=screen_size,resolution=resolution)
            request = scrapy.Request(url=url, callback=self.parse_param_url)
            request.meta['item'] = item
            yield request

    def parse_param_url(self,response):
        '''
        解析手机详情参数
        :param response:
        :return:
        '''

        item = response.meta['item']
        type1 = ""
        type2 = ""
        model = ""
        time = ""
        phone_color = ""
        phone_material = ""
        opreating_system = ""
        cpu_name = ""
        core_nums = ""
        sim = ""
        sim_max_nums = ""
        rom = ""
        ram = ""
        screen_material = ""
        battery = ""
        try:
            # 解析主要参数
            param_cs = response.xpath(".//div[@class='mainparam']/table[@class='paramtable-b']")[0].xpath("./tr")
            if len(param_cs) > 0:
                for tr in  param_cs:
                    ths = tr.xpath("./th")
                    for th in ths:
                        name = th.xpath("string(.)").extract()[0].strip()
                        value = th.xpath("./following-sibling::*")[0].xpath("string(.)").extract()[0].strip()
                        if name == "CPU型号".encode('utf-8'):
                            cpu_name = value
                        elif name == "处理器核心".encode('utf-8'):
                            core_nums = value
                        elif name == "操作系统版本".decode('utf-8'):
                            opreating_system = value
                        elif name == "RAM容量".encode('utf-8'):
                            ram = value
                        elif name == "ROM容量".encode('utf-8'):
                            rom = value
                        elif name == "电池容量(mAh)".encode('utf-8'):
                            battery = value

            # 解析基本参数
            param_basic = response.xpath(".//div[@class='mainparam']/table[@class='paramtable-b']")[1].xpath("./tr")
            if len(param_basic) > 0:
                for tr in param_basic:
                    ths = tr.xpath("./th")
                    for th in ths:
                        name = th.xpath("string(.)").extract()[0].strip()
                        value = th.xpath("./following-sibling::*")[0].xpath("string(.)").extract()[0].strip()
                        if name == '产品特性'.encode('utf-8'):
                            type1 = value
                        if name == '出品地区'.encode('utf-8'):
                            type2 = value
                        if name == '手机昵称'.encode('utf-8'):
                            model = value
                        if name == '上市时间'.encode('utf-8'):
                            time = value

            # 解析屏幕参数
            param_screen = response.xpath(".//div[@class='mainparam']/table[@class='paramtable-b']")[2].xpath("./tr")
            if len(param_screen) > 0:
                for tr in param_screen:
                    ths = tr.xpath("./th")
                    for th in ths:
                        name = th.xpath("string(.)").extract()[0].strip()
                        value = th.xpath("./following-sibling::*")[0].xpath("string(.)").extract()[0].strip()
                        if name == '屏幕材质'.encode('utf-8'):
                            screen_material = value
            # 解析网络制式
            param_network= response.xpath(".//div[@class='mainparam']/table[@class='paramtable-b']")[4].xpath("./tr")
            if len(param_network) > 0:
                for tr in param_network:
                    ths = tr.xpath("./th")
                    for th in ths:
                        name = th.xpath("string(.)").extract()[0].strip()
                        value = th.xpath("./following-sibling::*")[0].xpath("string(.)").extract()[0].strip()
                        if name == '手机制式'.encode('utf-8'):
                            sim = value
            # 解析外观参数
            param_outlook= response.xpath(".//div[@class='mainparam']/table[@class='paramtable-b']")[6].xpath("./tr")
            if len(param_outlook) > 0:
                for tr in param_outlook:
                    ths = tr.xpath("./th")
                    for th in ths:
                        name = th.xpath("string(.)").extract()[0].strip()
                        value = th.xpath("./following-sibling::*")[0].xpath("string(.)").extract()[0].strip()
                        if name == '机身颜色'.encode('utf-8'):
                            phone_color = value
                        if name == '外观特点'.encode('utf-8'):
                            phone_material = value
        except Exception,e:
            logging.exception(e)

        item['type1'] = type1
        item['type2'] = type2
        item['model'] = model
        item['time'] = time
        item['phone_color'] = phone_color
        item['phone_material'] = phone_material
        item['opreating_system'] = opreating_system
        item['cpu_name'] = cpu_name
        item['core_nums'] = core_nums
        item['sim'] = sim
        item['sim_max_nums'] = sim_max_nums
        item['rom'] = rom
        item['ram'] = ram
        item['screen_material'] = screen_material
        item['battery'] = battery
        item['data_source'] = '天极网'
        yield item


if __name__ == '__main__':
    # 启动tjw_spider爬虫
    process = CrawlerProcess(get_project_settings())
    process.crawl('tjw_spider')
    process.start()