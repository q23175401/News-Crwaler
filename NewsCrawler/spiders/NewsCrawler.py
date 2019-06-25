from bs4 import BeautifulSoup as bs
import requests
import re
import scrapy
import pandas as pd
from ..items import NewscrawlerItem

class NewsCrawler(scrapy.Spider):
    name = 'NewsCrawler'
    #start_urls = ['http://home.appledaily.com.tw/article/index/20160916/37384315/news/', 'http://www.chinatimes.com/newspapers/20120524000858-260109']
    
    def start_requests(self):
        self.News = pd.read_csv('NC_1.csv')
        news_urls = self.News['News_URL']
        start_urls = news_urls.tolist()
        return
        
    def parse(self, response):
        _, title, content = self.read_news(response.body, response.request.url)
        
        item = NewscrawlerItem()
        news_id="None"
        try:
            news_id = self.News.loc[self.News['News_URL']==response.request.url]['News_Index'].values[0]
        except:
            news_id = self.News.loc[self.News['News_URL']=="http"+response.request.url.strip('https')]['News_Index'].values[0]
        
        item['news_id'] = news_id
        item['news_url'] = response.request.url
        if _!=False:
            
            item['news_title'] = title
            item['news_content'] = content

        
            print(news_id)
            
            return item
        else:
            item['news_title']   = ""
            item['news_content'] = ""
            return 
        # print(title+content)
        
    def apple_reader(self, body, url):
        # 有分兩種 home 跟其他版
        res = bs(body, features='lxml')
        
        title = ""
        content = ""
        if url.find('home.appledaily.com.tw/') != -1:
            title = ('標題: '+ res.select('.ncbox_cont h1')[0].text.strip('\n')+'\n')
            for p in res.select('.ncbox_cont p'):
                if len(p) !=0:
                    paragraph = (p.text.strip('\n').strip() + '\n')
                    content += paragraph
        else:
            title = ('標題: '+res.select('.ndArticle_leftColumn h1')[0].text.strip('\n')+" "+
                  res.select('.ndArticle_leftColumn h2')[0].text.strip('\n')+'\n')
            for p in res.select('.ndArticle_margin p'):
                if len(p) !=0:
                    paragraph = (p.text.strip('\n').strip() + '\n')
                    content += paragraph
        return title, content

    def liberty_reader(self, body):
        res = bs(body, features='lxml')
        
        title = ('標題: '+res.select('.whitecon h1')[0].text.strip('\n')+'\n')
        # print(title)
        content = ""
        for p in res.select('.whitecon p'):
            if len(p.text) !=0 and p.text.find('想看更多新聞嗎？現在用APP看新聞還可以抽獎')==-1 and p.text.find('／特稿')==-1:
                paragraph = (p.text.strip('\n').strip() + '\n')
                content += paragraph
                # print(paragraph)
        return title, content


    def chinatimes_reader(self, body):
        res = bs(body, features='lxml')
        
        title = ('標題: '+res.select('.article-title')[0].text.strip('\n')+'\n')
        # print(title)
        content = ""
        for p in res.select('.article-body p'):
            if len(p.text) != 0 and p.text.find('(中時電子報)')==-1:
                paragraph = (p.text.strip('\n').strip() + '\n')
                content += paragraph
                # print(paragraph)
        return title, content

    def tvbs_reader(self, body):
        res = bs(body, features='lxml')
        
        title = ('標題: '+res.select('.title h1')[0].text.strip('\n')+'\n')
        # print(title)
        content = ""
        for p in res.select('#news_detail_div'):
            if len(p.text) != 0:
                paragraph = (p.text.strip('\n').strip() + '\n')
                content += paragraph
                # print(paragraph)
        return title, content

    def udn_reader(self, body):
        res = bs(body, features='lxml')

        title = ('標題: '+res.select(".story_art_title")[0].contents[0].strip('\n')+'\n')
        # print(title)
        content = ""
        for p in res.select('#story_body_content p'):
            if len(p.text) != 0:
                paragraph = (p.text.strip('\n').strip() + '\n')
                content += paragraph
                # print(paragraph)
        return title, content

    def read_news(self, body, url):
        titie = ""
        content = ""
        try:
            if url.find('.appledaily.com')!=-1:
                # print('蘋果日報新聞')
                titie, content = self.apple_reader(body, url)
            elif url.find('news.ltn.com.tw')!=-1:
                # print('自由時報新聞')
                titie, content = self.liberty_reader(body)
            elif url.find('www.chinatimes.com')!=-1:
                # print('中國時報新聞')
                titie, content = self.chinatimes_reader(body)
            elif url.find('news.tvbs.com.tw')!=-1:
                # print('TVBS新聞')
                titie, content = self.tvbs_reader(body)
            elif url.find('udn.com/'):
                # print('聯合新聞網新聞
                titie, content = self.udn_reader(body)
            else:
                print("沒看過的新聞來源: " + url)
                return False, titie, content
        except Exception as e:
            print(e)
            print("讀取新聞失敗: " + url)
            return False, titie, content
        return True, titie, content
if __name__ == '__main__':
    url = 'http://home.appledaily.com.tw/article/index/20160916/37384315/news/'
    crawler = NewsCrawler()
    _, title, content = crawler.read_news(url)
    print(title+content)
    