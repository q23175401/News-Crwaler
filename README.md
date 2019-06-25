# News-Crwaler
用Python 寫的新聞爬蟲

這是參加AI CUP 新聞檢索技術應用賽所寫的 News Crawler

主要爬:
  蘋果新聞
  聯合新聞
  中國時報
  自由時報
  TVBS

說明:
  1. 透過scrapy將request分成不同的thread同時爬取NC_1.csv的新聞
  2. 將爬下來的新聞透過JIJIESQLDB存到MySQL裡面
  3. 每個新聞抓取標題、內容
