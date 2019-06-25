# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from JIJIESQL import JIJIESQLDB 

class NewscrawlerPipeline(object):
    def open_spider(self, spider):

        self.db = JIJIESQLDB()

    def process_item(self, item, spider):
        news_dict = {
            'news_id'      : item['news_id'],
            'news_url'     : item['news_url'],
            'news_title'   : item['news_title'],
            'news_content' : item['news_content']
        }
        
        
        if news_dict['news_title']!="" and news_dict['news_id'] != "None":
            self.db.insert_news(news_dict)
        
        return item

    def close_spider(self, spider):
        del self.db