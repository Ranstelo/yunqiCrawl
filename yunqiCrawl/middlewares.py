# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from yunqiCrawl import settings
import random


class RandomUserAgent(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls,crawler ):
        return cls(settings.USER_AGENTS)

    def process_request(self,request,spider):
        request.headers["User-Agent"] = random.choice(self.agents)
        print(request.headers["User-Agent"])


