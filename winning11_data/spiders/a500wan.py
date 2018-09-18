# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from winning11_data.items import Winning11DataItem
from datetime import datetime,timedelta

def toTs(date_str):
    import time
    return time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M"))

class winSpider(Spider):  
    name = "win"  
    allowed_domains = ["odds.500.com"]
    start_urls = []
    start_date = datetime(2018,8,18)
    end_date = datetime(2018,8,20)
    while start_date<end_date:
        start_urls.append(start_date.strftime("http://odds.500.com/index_jczq_%Y-%m-%d.shtml"))
        start_date+=timedelta(1)
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        parse_item = Winning11DataItem()
        items = response.xpath('//div[@id="bd"]/table//tbody[@id="main-tbody"]/tr')
        import re
        date_str = re.findall("http://odds.500.com/index_jczq_(.*?).shtml",response.url)[0]
        date_arr = date_str.split('-')
        for item in items:
            try:
                teams = item.xpath('.//a[@class="team_link"]/@title').extract()
                if len(teams) == 0:
                    continue
                parse_item["game_type"] = item.xpath('.//a/@title').extract()[0].encode('utf-8')
                parse_item["home_team"] = teams[0].encode('utf-8')
                parse_item["guest_team"] = teams[1].encode('utf-8')
                parse_item["score"] = item.xpath('.//span[@class="red"]/text()').extract()[0].encode('utf-8')
                details = item.xpath('.//td/text()').extract()
                parse_item["match_round"] = details[0].encode('utf-8')
                parse_item["match_time"] = details[1].encode('utf-8')
                parse_item["match_time"] = date_arr[0]+'-'+parse_item["match_time"]
                parse_item["match_time_ts"] = toTs(parse_item["match_time"])
                parse_item["gamble_company"] = details[2].encode('utf-8')
                parse_item["home_water"] = details[3].encode('utf-8')
                parse_item["match_gain"] = details[4].encode('utf-8')
                parse_item["guest_water"] = details[5].encode('utf-8')
                parse_item["win_rate"] = details[6].encode('utf-8')
                parse_item["draw_rate"] = details[7].encode('utf-8')
                parse_item["lost_rate"] = details[8].encode('utf-8')
                parse_item["pay_rate"] = details[9].encode('utf-8')
                team_urls = item.xpath('.//a[@class="team_link"]/@href').extract()
                yield parse_item
            except:
                continue
