# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from winning11_data.items import PredictDataItem
from datetime import datetime,timedelta
import re
import time
from scrapy.http import HtmlResponse
import random
class predictSpider(Spider):  
    name = "predict"  
    allowed_domains = []
    start_urls = []
    start_date = datetime.now()+timedelta(hours=12)
    end_date = start_date + timedelta(1)
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
            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        #parse rate historys
        self.browser.get(response.url)
        elements = self.browser.find_elements_by_xpath("//tr/td[@class='cur-pointer']")
        match_total = int(self.browser.find_element_by_id("game-total-count").text)
        cnt = 2
        rates_delta = []
        if len(elements) != 8*match_total:
            print "lack of Info!!!%d elements for %d matches!!!"%(len(elements),match_total)
            #return
        while cnt<len(elements):
            element = elements[cnt]
            try:
                element.click()
            except:
                elements = self.browser.find_elements_by_xpath("//tr/td[@class='cur-pointer']")
                continue
            time.sleep(random.randint(3,5))
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

        parse_item = PredictDataItem()
        items = response.xpath('//div[@id="bd"]/table//tbody[@id="main-tbody"]/tr')
        idx = 0
        for item in items:
            try:
                teams = item.xpath('.//a[@class="team_link"]/@title').extract()
                team_urls = item.xpath('.//a[@class="team_link"]/@href').extract()
                if len(teams) == 0 or len(team_urls) == 0:
                    continue
                parse_item["game_type"] = item.xpath('.//a/@title').extract()[0].encode('utf-8')
                parse_item["home_team"] = teams[0].encode('utf-8')
                parse_item["guest_team"] = teams[1].encode('utf-8')
                details = item.xpath('.//td/text()').extract()
                if details[2].encode('utf-8') != "VS":
                    continue
                for it in details:
                    print it.encode('utf-8')
                parse_item["match_round"] = details[0].encode('utf-8')
                parse_item["match_time"] = details[1].encode('utf-8')
                parse_item["gamble_company"] = details[3].encode('utf-8')
                parse_item["home_water"] = details[4].encode('utf-8')
                parse_item["match_gain"] = details[5].encode('utf-8')
                parse_item["guest_water"] = details[6].encode('utf-8')
                parse_item["win_rate"] = details[7].encode('utf-8')
                parse_item["draw_rate"] = details[8].encode('utf-8')
                parse_item["lost_rate"] = details[9].encode('utf-8')
                parse_item["pay_rate"] = details[10].encode('utf-8')
                parse_item["home_url"] = team_urls[0]
                parse_item["guest_url"] = team_urls[1]
                parse_item["win_rate_max"] = str(rates_delta[idx][0][0])
                parse_item["win_rate_min"] = str(rates_delta[idx][0][1])
                parse_item["draw_rate_max"] = str(rates_delta[idx][1][0])
                parse_item["draw_rate_min"] = str(rates_delta[idx][1][1])
                parse_item["lost_rate_max"] = str(rates_delta[idx][2][0])
                parse_item["lost_rate_min"] = str(rates_delta[idx][2][1])
                idx += 1
                yield scrapy.Request(parse_item["home_url"], meta=parse_item,callback=self.parse_homeurl, dont_filter=True)
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
        del parse_item["download_latency"]
        del parse_item["download_slot"]
        del parse_item["download_timeout"]
        del parse_item["depth"]
        print parse_item
        yield parse_item
