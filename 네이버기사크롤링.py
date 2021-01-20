import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

class Article():
    
    def __init__(self, keyword, page_range):
        self.keyword = keyword
        self.page_range = page_range
        self.url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&start={}'
        self.headers = {'User-Agent':'Chrome/51.0.2704.103'}
        self.list_news = "ul.list_news > li"
        self.title_news = "a.news_tit"
        self.press_news = "a.info.press"
        self.text_news = "a.api_txt_lines.dsc_txt_wrap"
        
        
    def html_parse(self):
        if int(self.page_range) >= 1:
            html_box = []
            for i in tqdm(range(self.page_range), mininterval = 1, desc = 'Scrapping html'):
                self.url = self.url.format(self.keyword, i * 10 + 1)
                root = requests.get(self.url, headers = self.headers)
                html = BeautifulSoup(root.text, 'html.parser')
                html_box.append(html)
            return html_box
        else:
            print("Page_range is out of bounds or Page_range has something wrong")
            
            
    def crawling(self):
        html = Article.html_parse(self)
        news_box = {}
        title, press, text = [], [], []
        for i in tqdm(range(len(html)), mininterval = 0.1, desc = 'Parsing Article Info'):
            articles = html[i].select(self.list_news)
            for ar in articles:
                title_ = ar.select_one(self.title_news).text
                source = ar.select_one(self.press_news).text
                textline = ar.select_one(self.text_news).text

                title.append(title_)
                press.append(source)
                text.append(textline)

            news_box['title'] = title
            news_box['press'] = press
            news_box['text'] = text
        
        DF = pd.DataFrame(news_box, columns=['press', 'title', 'text'])
        
        return DF

if __name__ == "__main__":
    article = Article('날씨', 5)
    news_data =article.crawling()
    print(news_data.tail())
    #if you want to save -> activate this codes
    #directory = 'C:/My/Directory/'
    #news_data.to_csv(f"{directory}/{article.keyword}_news.csv", encoding = 'utf-8', index = False)
