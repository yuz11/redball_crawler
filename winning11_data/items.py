# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Winning11DataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_type = scrapy.Field()
    home_team = scrapy.Field()
    guest_team = scrapy.Field()
    score = scrapy.Field()
    match_round = scrapy.Field()
    match_time = scrapy.Field()
    gamble_company = scrapy.Field()
    home_water = scrapy.Field()
    match_gain = scrapy.Field()
    guest_water = scrapy.Field()
    win_rate = scrapy.Field()
    draw_rate = scrapy.Field()
    lost_rate = scrapy.Field()
    pay_rate = scrapy.Field()

class PredictDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_type = scrapy.Field()
    home_team = scrapy.Field()
    guest_team = scrapy.Field()
    match_round = scrapy.Field()
    match_time = scrapy.Field()
    gamble_company = scrapy.Field()
    home_water = scrapy.Field()
    match_gain = scrapy.Field()
    guest_water = scrapy.Field()
    win_rate = scrapy.Field()
    draw_rate = scrapy.Field()
    lost_rate = scrapy.Field()
    pay_rate = scrapy.Field()
    home_url = scrapy.Field()
    guest_url = scrapy.Field()
    home_last_win = scrapy.Field()
    home_last_draw = scrapy.Field()
    home_last_lost = scrapy.Field()
    home_last_goal = scrapy.Field()
    home_last_gain = scrapy.Field()
    home_value = scrapy.Field()
    guest_last_win = scrapy.Field()
    guest_last_draw = scrapy.Field()
    guest_last_lost = scrapy.Field()
    guest_last_goal = scrapy.Field()
    guest_last_gain = scrapy.Field()
    guest_value = scrapy.Field()

class GameDetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_type = scrapy.Field()
    home_team = scrapy.Field()
    guest_team = scrapy.Field()
    score = scrapy.Field()
    match_round = scrapy.Field()
    match_time = scrapy.Field()
    gamble_company = scrapy.Field()
    home_water = scrapy.Field()
    match_gain = scrapy.Field()
    guest_water = scrapy.Field()
    win_rate = scrapy.Field()
    draw_rate = scrapy.Field()
    lost_rate = scrapy.Field()
    pay_rate = scrapy.Field()
    home_url = scrapy.Field()
    guest_url = scrapy.Field()
    home_last_win = scrapy.Field()
    home_last_draw = scrapy.Field()
    home_last_lost = scrapy.Field()
    home_last_goal = scrapy.Field()
    home_last_gain = scrapy.Field()
    home_value = scrapy.Field()
    guest_last_win = scrapy.Field()
    guest_last_draw = scrapy.Field()
    guest_last_lost = scrapy.Field()
    guest_last_goal = scrapy.Field()
    guest_last_gain = scrapy.Field()
    guest_value = scrapy.Field()