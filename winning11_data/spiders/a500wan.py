# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from winning11_data.items import Winning11DataItem
from datetime import datetime,timedelta
import time
from scrapy.http import HtmlResponse
import random

def toTs(date_str):
    return time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M"))

class winSpider(Spider):
    name = "games"  
    allowed_domains = []
    start_urls = []
    start_date = datetime(2018,8,31)
    end_date = datetime(2018,10,28)
    while start_date<end_date:
        start_urls.append(start_date.strftime("http://odds.500.com/index_jczq_%Y-%m-%d.shtml"))
        start_date+=timedelta(1)
    
    def start_requests(self):
        #init selenium
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
        from selenium.webdriver.common.keys import Keys #引入keys类操作
        import time
        from scrapy.http import HtmlResponse

        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(chrome_options=options)

        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        #parse rate historys
        self.browser.get(response.url)
        elements = self.browser.find_elements_by_xpath("//tr/td[@class='cur-pointer']")
        match_total = int(self.browser.find_element_by_id("game-total-count").text)
        cnt = 2
        rates_delta = []
        if len(elements) != 8*match_total:
            print "lack of Info!!!%d elements for %d matches!!!"%(len(elements),match_total)
            return
        while cnt<len(elements):
            element = elements[cnt]
            element.click()
            time.sleep(random.randint(5,10))
            resp = HtmlResponse(url=response.url, body=self.browser.page_source, encoding='utf-8',status=200)
            match_name = resp.xpath('//div[@class="tips_box"]/div[@class="tips_title"]/h2/text()').extract()[0]
            teams = match_name.split("vs")
            print teams[0].strip(" ").encode('utf-8')
            items = resp.xpath('//div[@class="tips_box"]/div[@class="tips_table"]/table[@class="pub_table"]//tbody/tr')
            home_rate_delta=[]
            draw_rate_delta=[]
            guest_rate_delta=[]
            for item in items:
                row = item.extract()
                import re
                details = re.findall("\d+.?\d*",row)
                try:
                    home_rate_delta.append(float(details[0]))
                    draw_rate_delta.append(float(details[1]))
                    guest_rate_delta.append(float(details[2]))
                except Exception as e:
                    print details
                    time.sleep(random.randint(300,900))
                    continue
            try:
                home_delta = (max(home_rate_delta),min(home_rate_delta))
                draw_delta = (max(draw_rate_delta),min(draw_rate_delta))
                guest_delta = (max(guest_rate_delta),min(guest_rate_delta))
                rates_delta.append([home_delta,draw_delta,guest_delta])
                cnt+=8
            except:
                return
        print len(rates_delta)
        
        #parse final rates
        parse_item = Winning11DataItem()
        items = response.xpath('//div[@id="bd"]/table//tbody[@id="main-tbody"]/tr')
        import re
        date_str = re.findall("http://odds.500.com/index_jczq_(.*?).shtml",response.url)[0]
        date_arr = date_str.split('-')
        idx = 0
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
                parse_item["win_rate_max"] = rates_delta[idx][0][0]
                parse_item["win_rate_min"] = rates_delta[idx][0][1]
                parse_item["draw_rate_max"] = rates_delta[idx][1][0]
                parse_item["draw_rate_min"] = rates_delta[idx][1][1]
                parse_item["lost_rate_max"] = rates_delta[idx][2][0]
                parse_item["lost_rate_min"] = rates_delta[idx][2][1]
                idx+=1
                yield parse_item
            except Exception as e:
                idx+=1
                print e
                continue
