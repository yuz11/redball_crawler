# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from winning11_data.items import GameDetailItem
from datetime import datetime,timedelta
import re
class detailSpider(Spider):  
    name = "detail"  
    allowed_domains = []
    start_urls = []
    start_date = datetime.now() - timedelta(1)
    end_date = datetime.now()
    while start_date<end_date:
        start_urls.append(start_date.strftime("http://odds.500.com/index_jczq_%Y-%m-%d.shtml"))
        start_date+=timedelta(1)
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        parse_item = GameDetailItem()
        items = response.xpath('//div[@id="bd"]/table//tbody[@id="main-tbody"]/tr')
        for item in items:
            try:
                teams = item.xpath('.//a[@class="team_link"]/@title').extract()
                team_urls = item.xpath('.//a[@class="team_link"]/@href').extract()
                if len(teams) == 0 or len(team_urls) == 0:
                    continue
                parse_item["game_type"] = item.xpath('.//a/@title').extract()[0].encode('utf-8')
                parse_item["home_team"] = teams[0].encode('utf-8')
                parse_item["guest_team"] = teams[1].encode('utf-8')
                parse_item["score"] = item.xpath('.//span[@class="red"]/text()').extract()[0].encode('utf-8')
                details = item.xpath('.//td/text()').extract()
                parse_item["match_round"] = details[0].encode('utf-8')
                parse_item["match_time"] = details[1].encode('utf-8')
                parse_item["gamble_company"] = details[2].encode('utf-8')
                parse_item["home_water"] = details[3].encode('utf-8')
                parse_item["match_gain"] = details[4].encode('utf-8')
                parse_item["guest_water"] = details[5].encode('utf-8')
                parse_item["win_rate"] = details[6].encode('utf-8')
                parse_item["draw_rate"] = details[7].encode('utf-8')
                parse_item["lost_rate"] = details[8].encode('utf-8')
                parse_item["pay_rate"] = details[9].encode('utf-8')
                parse_item["home_url"] = team_urls[0]
                parse_item["guest_url"] = team_urls[1]
                yield scrapy.Request(parse_item["home_url"], meta=parse_item,callback=self.parse_homeurl, dont_filter=True)
                #yield scrapy.Request(parse_item["home_url"], meta={'item': parse_item,'splash': {'args': {'wait': 0.5}}},callback=self.parse_homeurl)
            except:
                continue
    def parse_homeurl(self, response):
        #parse home url
        parse_item = response.meta
        items = response.xpath('//div[@class="lcur_chart"]/table[@class="lwfull"]/tr/td[@class="lcur_chart_zj"]/p/span').extract()
        if len(items) != 5:
            print "home url Not enough data"
            return
        parse_item["home_last_win"] = re.findall("\d+",items[0])[0]
        parse_item["home_last_draw"] = re.findall("\d+",items[1])[0]
        parse_item["home_last_lost"] = re.findall("\d+",items[2])[0]
        parse_item["home_last_goal"] = re.findall("\d+",items[3])[0]
        parse_item["home_last_gain"] = re.findall("\d+",items[4])[0]
        #team value
        try:
            team_info = response.xpath('//div[@class="lwrap"]/div[@class="lmain"]/div[@class="lmain_in clearfix"]/div[@class="clearfix"]/div[@class="lcontent"]/div[@class="lqiud_summary clearfix"]/div[@class="itm_bd"]/table').extract()
            parse_item["home_value"] = re.findall(ur'\u7403\u961f\u8eab\u4ef7\uff1a\u20ac (.*)\u4e07',team_info[0])[0]
        except:
            parse_item["home_value"] = "0"
        yield scrapy.Request(parse_item["guest_url"], meta=parse_item, callback=self.parse_guesturl, dont_filter=True)

        #yield scrapy.Request(parse_item["guest_url"], meta={'item': parse_item,'splash': {'args': {'wait': 0.5}}}, callback=self.parse_guesturl)

    def parse_guesturl(self, response):
        #parse guest url
        parse_item = response.meta
        items = response.xpath('//div[@class="lcur_chart"]/table[@class="lwfull"]/tr/td[@class="lcur_chart_zj"]/p/span').extract()
        if len(items) != 5:
            print "guest url Not enough data"
            return
        parse_item["guest_last_win"] = re.findall("\d+",items[0])[0]
        parse_item["guest_last_draw"] = re.findall("\d+",items[1])[0]
        parse_item["guest_last_lost"] = re.findall("\d+",items[2])[0]
        parse_item["guest_last_goal"] = re.findall("\d+",items[3])[0]
        parse_item["guest_last_gain"] = re.findall("\d+",items[4])[0]
        try:
            team_info = response.xpath('//div[@class="lwrap"]/div[@class="lmain"]/div[@class="lmain_in clearfix"]/div[@class="clearfix"]/div[@class="lcontent"]/div[@class="lqiud_summary clearfix"]/div[@class="itm_bd"]/table').extract()
            parse_item["guest_value"] = re.findall(ur'\u7403\u961f\u8eab\u4ef7\uff1a\u20ac (.*)\u4e07',team_info[0])[0]
        except:
            parse_item["guest_value"] = "0"
        yield parse_item

