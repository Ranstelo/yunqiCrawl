# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from yunqiCrawl.items import YunqiBookListItem
import re

class YunqicrawlPipeline(object):

    # def __init__(self, mongo_uri, mongo_db, replicaset):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db
    #     self.replicaset = replicaset
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(mongo_uri=crawler)
    def open_spider(self, spider):
        self.client = MongoClient()
        self.collection = self.client["yunqi"]["book"]

    def close_spider(self,spider):
        self.client.close()


    def process_item(self, item, spider):
        if isinstance(item,YunqiBookListItem):
            # pass
            # self._precess_booklist_item(item)
        # else:
            # print("==================")
            # print(item)
            self._precess_bookeDetail_item(item)
        return item


    def _precess_booklist_item(self, item):
        """
        处理小说信息
        :param item:
        :return:
        """
        self.collection.insert(dict(item))


    def _precess_bookeDetail_item(self,item):
        """
        处理小说热度
        :param item:
        :return:
        """
        pattern = re.compile("\d+")

        item["novelLabel"] = item["novelLabel"].strip().replace("\n","")

        match = pattern.search(item["novelAllClick"])
        item["novelAllClick"] = match.group() if match else item["novelAllClick"]

        match = pattern.search(item["novelMonthClick"])
        item["novelMonthClick"] = match.group() if match else item["novelMonthClick"]

        match = pattern.search(item["novelWeekClick"])
        item["novelWeekClick"] = match.group() if match else item["novelWeekClick"]

        match = pattern.search(item["novelAllPopular"])
        item["novelAllPopular"] = match.group() if match else item["novelAllPopular"]

        match = pattern.search(item["novelMonthPopular"])
        item["novelMonthPopular"] = match.group() if match else item["novelMonthPopular"]

        match = pattern.search(item["novelWeekPopular"])
        item["novelWeekPopular"] = match.group() if match else item["novelWeekPopular"]

        match = pattern.search(item["novelAllComm"])
        item["novelAllComm"] = match.group() if match else item["novelAllComm"]

        match = pattern.search(item["novelMonthComm"])
        item["novelMonthComm"] = match.group() if match else item["novelMonthComm"]

        match = pattern.search(item["novelWeekComm"])
        item["novelWeekComm"] = match.group() if match else item["novelWeekComm"]

        self.collection.insert(dict(item))













