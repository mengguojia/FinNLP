import warnings
warnings.filterwarnings("ignore")
import requests
from lxml import etree
from tqdm import tqdm
import pandas as pd
import json
import time
import datetime
from finnlp.data_sources.social_media._base import Social_Media_Downloader

# TODO:
# 1. Contents

class Eastmoney_Streaming(Social_Media_Downloader):
    def __init__(self, args = {}):
        super().__init__(args)
        self.dataframe = pd.DataFrame()

    def download_streaming_stock(self, keyword = "600519", end_time = datetime.date.today().isoformat(),rounds = 100, delay = 0.5):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        }
        print('Downloading ...', end =' ')
        for page in range(rounds):
            url = f"https://guba.eastmoney.com/list,{keyword},f_{page+1}.html"
            resp = self._request_get(url=url, headers=headers)
            if resp is None:
                continue

            res = etree.HTML(resp.text)
            res = res.xpath("//script")[3].xpath("text()")[0]
            article_list, other_list = res.split('var article_list=')[1].strip(";").split(';    var other_list=')
            article_list = json.loads(article_list)
            other_list = json.loads(other_list.split(';var')[0])
            tmp = article_list['re']
            tmp2 = other_list['re']
            for i in tmp2:
                tmp.remove(i)
            df = pd.DataFrame(tmp)
            self.gather_content(df['post_id'],keyword,delay)
            #self.dataframe = pd.concat([self.dataframe, tmp])

            print('第', page, '页')
            if datetime.datetime.fromisoformat(df['post_publish_time'].iloc[-1])<datetime.datetime.fromisoformat(end_time):
                break
            time.sleep(delay)
        
        self.dataframe = self.dataframe.reset_index(drop= True)

    def gather_content(self, post_id, keyword, delay = 0.01):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        }
        content_list = []
        for post in tqdm(post_id, desc= "Gathering news contents"):
            if 'ad' in str(post):
                continue
            url = f"https://guba.eastmoney.com/news,{keyword},{post}.html"
            resp = self._request_get(url=url, headers=headers)
            if resp is None:
                continue
            res = etree.HTML(resp.text)
            scr = res.xpath("//script/text()")
            for i in scr:
                if 'post_article=' in i:
                    article = i.split('post_article=')[1].strip()
                    article = json.loads(article)
                    content_list.append(article)
                    break

            time.sleep(delay)

        content = pd.DataFrame(content_list)
        self.dataframe = pd.concat([self.dataframe, content])



        