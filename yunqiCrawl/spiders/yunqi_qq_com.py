# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yunqiCrawl.items import YunqiBookListItem
from copy import deepcopy
from scrapy_redis.spiders import RedisCrawlSpider

class YunqiQqComSpider(RedisCrawlSpider):

    name = 'yunqi'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n30p1']
    redis_key = "yunqi"

    rules = (
        Rule(LinkExtractor(allow=r'bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):
        """
        图书列表
        :param response:
        :return:
        """
        books = response.xpath("//div[@class='book']")
        for book in books:
            novelImageUrl = book.xpath("./a/img/@src").extract_first()
            novelId = book.xpath("./div[@class='book_info']/h3/a/@id").extract_first()
            novelName = book.xpath("./div[@class='book_info']/h3/a/text()").extract_first()
            novelLink = book.xpath("./div[@class='book_info']/h3/a/@href").extract_first()
            novelInfos = book.xpath("./div[@class='book_info']/dl/dd[@class='w_auth']")

            if len(novelInfos) > 4:
                novelAuthor = novelInfos[0].xpath('./a/text()').extract_first()
                novelType = novelInfos[1].xpath('./a/text()').extract_first()
                novelStatus = novelInfos[2].xpath('./text()').extract_first()
                novelUpdateTime = novelInfos[3].xpath('./text()').extract_first()
                novelWords = novelInfos[4].xpath('./text()').extract_first()
            else:
                novelAuthor = ''
                novelType = ''
                novelStatus = ''
                novelUpdateTime = ''
                novelWords = 0

            bookListItem = YunqiBookListItem(novelId=novelId,
                                             novelName=novelName,
                                             novelLink=novelLink,
                                             novelAuthor=novelAuthor,
                                             novelType=novelType,
                                             novelStatus=novelStatus,
                                             novelUpdateTime=novelUpdateTime,
                                             novelWords=novelWords)

            yield scrapy.Request(url=novelLink,callback=self.parse_book_detail,meta={"bookListItem":deepcopy(bookListItem)})


    def parse_book_detail(self, response):
        """
         图书详情页
        :param response:
        :return:
        """
        bookListItem = response.meta["bookListItem"]
        # novelId = bookListItem
        bookListItem["novelLabel"] = response.xpath("//div[@class='tags']/text()").extract_first()
        bookListItem["novelAllClick"] = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[1]/text()").extract_first()
        bookListItem["novelAllPopular"] = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[2]/text()").extract_first()
        bookListItem["novelAllComm"] = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[3]/text()").extract_first()
        bookListItem["novelMonthClick"] = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[1]/text()").extract_first()
        bookListItem["novelMonthPopular"] = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[2]/text()").extract_first()
        bookListItem["novelMonthComm"] = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[3]/text()").extract_first()
        bookListItem["novelWeekClick"] = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[1]/text()").extract_first()
        bookListItem["novelWeekPopular"] = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[2]/text()").extract_first()
        bookListItem["novelWeekComm"] = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[3]/text()").extract_first()
        bookListItem["novelCommentNum"] = response.xpath(".//*[@id='novelInfo_commentCount']/text()").extract_first()

        # bookListItem = bookListItem(novelLabel=novelLabel,
        #                             novelAllClick=novelAllClick,
        #                             novelAllPopular=novelAllPopular,
        #                             novelAllComm=novelAllComm,
        #                             novelMonthClick=novelMonthClick,
        #                             novelMonthPopular=novelMonthPopular,
        #                             novelMonthComm=novelMonthComm,
        #                             novelWeekClick=novelWeekClick,
        #                             novelWeekPopular=novelWeekPopular,
        #                             novelWeekComm=novelWeekComm,
        #                             novelCommentNum=novelCommentNum)

        yield bookListItem












