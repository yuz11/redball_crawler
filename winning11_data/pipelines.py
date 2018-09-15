# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from winning11_data.dbs import NemoCfgMongoClient
from winning11_data.items import Winning11DataItem,PredictDataItem,GameDetailItem

class Winning11DataPipeline(object):
    def open_spider(self,spider):
        self.client = NemoCfgMongoClient()
        #self.client.data_500wan.drop_collection("games")

    def close_spider(self,spider):
        self.client.close()
    def process_item(self, item, spider):
        if isinstance(item,Winning11DataItem):
            item_dict = {}
            for key,value in item.items():
            	item_dict[key] = value
            self.client.data_500wan.recent_games.insert(item_dict)
        elif isinstance(item,PredictDataItem):
            item_dict = {}
            for key,value in item.items():
                item_dict[key] = value
            self.client.data_500wan.predict.insert(item_dict)
        else:
            item_dict = {}
            for key,value in item.items():
                item_dict[key] = value
            self.client.data_500wan.detail_games.insert(item_dict)