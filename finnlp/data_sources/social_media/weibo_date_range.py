from finnlp.data_sources.social_media._base import Social_Media_Downloader

from tqdm import tqdm
from lxml import etree
import pandas as pd
import numpy as np
import random
import requests
import datetime
import time
import json
import re

class Weibo_Date_Range(Social_Media_Downloader):
    def __init__(self, args = {}):
        super().__init__(args)
        if "cookies" not in args.keys():
            raise ValueError("You need first log in at https://weibo.com/ and then copy you cookies and use it as the [value] of [key] \'cookies\' ")
        self.cookies = args["cookies"]
        self.dataframe = pd.DataFrame()

    def _get_cookies(self):
        assert type(self.cookies) == list
        return random.choice(self.cookies)

    def download_date_range_stock(self, start_date, end_date, start_hour= 0,end_hour = 0,stock = "茅台", delay = 0.01):
        start_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        start_time_range = [start_dt + datetime.timedelta(hours=i) for i in range(int((end_dt - start_dt).days) * 24 + 1)]
        for i in tqdm(start_time_range, desc = "Downloading by dates..."):
            self._gather_one_hour(i.strftime('%Y-%m-%d'), (i+datetime.timedelta(hours=1)).strftime('%Y-%m-%d'), i.strftime('%H'), (i+datetime.timedelta(hours=1)).strftime('%H'), stock, delay)
        self.dataframe = self.dataframe.reset_index(drop = True)

    def _gather_one_hour(self, start_date, end_date, start_hour, end_hour, stock ="茅台", delay = 0.01):

        # first page
        all_urls = self._gather_first_page(start_date, end_date, start_hour, end_hour, stock, delay)
        # another pages
        if len(all_urls)>1:
            base_url=  "https://s.weibo.com/"
            for url_new in all_urls[1:]:
                url_new = base_url + url_new
                self._gather_other_pages(start_date, url_new, delay)
                print('第', url_new[-1], '页')
         
    def _gather_first_page(self,start_date, end_date, start_hour, end_hour, stock = "茅台", delay = 0.01):  
        
        headers = {
            "cookie": self._get_cookies(),
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            }
        
        params = {
            "q": stock,
            "typeall": "1",
            "suball": "1",
            "timescope":f"custom:{start_date}-{start_hour}:{end_date}-{end_hour}",
            "Refer":"g",
            "page":"1"
        }

        url = f"https://s.weibo.com/weibo"
        resp = self._request_get(url, headers=headers, params = params)
        
        if resp is None:
            return "Error"

        if "passport.weibo.com" in resp.url:
            raise ValueError("Your cookies is useless. Please first log in at https://weibo.com/ and then copy you cookies and use it as the [value] of [key] \'cookies\' ")

        res = etree.HTML(resp.content)
        # get all pages
        all_pages = res.xpath('//*[@id="pl_feedlist_index"]/div[3]/div[1]/span/ul/li//@href')
        items = res.xpath('//div[@class="card-wrap"]')
        df_list = []
        for i in items:
            try:
                content = i.xpath('.//div[@class="content"]//p//text()')
                content = ''.join(content)
                content = content.replace('\n',"")
                content = content.replace(' ',"")
                content = content.replace('\u200b',"")
            except:
                continue

            try:
                source = i.xpath('.//div[@class="from"]//a')
                date_content = source[0].text
                date_content = date_content.replace('\n',"")
                date_content = date_content.replace(' ',"")
                link = 'https:'+source[0].xpath('.//@href')[0].split('?')[0]
            except:
                date_content = np.nan
                link = None

            try:
                user = i.xpath('.//div[@class="content"]//p//@nick-name')[0]
            except:
                user = np.nan

            try:
                card_info = i.xpath(
                    './/div[@class="card-act"]//a[@class="woo-box-flex woo-box-alignCenter woo-box-justifyCenter"]')
                forward = ''.join(card_info[0].xpath('.//text()'))
                forward = forward.replace('\n', "")
                forward = forward.replace(' ', "")
                if not forward.isdecimal():
                    forward = 0
                comment = ''.join(card_info[1].xpath('.//text()'))
                comment = comment.replace('\n', "")
                comment = comment.replace(' ', "")
                if not comment.isdecimal():
                    comment = 0
                like = ''.join(card_info[2].xpath('.//text()'))
                like = like.replace('\n', "")
                like = like.replace(' ', "")
                if not like.isdecimal():
                    like = 0
            except:
                forward = np.nan
                comment = np.nan
                like = np.nan

            
            tmp = pd.DataFrame([start_date, date_content, user, content, link, forward, comment, like]).T
            tmp.columns = ["date","date_content", "user", "content", "link", "forward", "comment", "like"]
            df_list.append(tmp)
        if df_list:
            self.dataframe = pd.concat([self.dataframe, pd.concat(df_list)])

        print(f"采集完成{start_date}-{start_hour}:{end_date}-{end_hour}")
        time.sleep(delay)

        return all_pages
    
    def _gather_other_pages(self, date, url, delay = 0.01):
        
        headers = {
            "cookie": self._get_cookies(),
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", 
            }
        
        resp = self._request_get(url, headers=headers)

        if resp is None:
            return "Error"

        if "passport.weibo.com" in resp.url:
            raise ValueError("Your cookies is useless. Please first log in at https://weibo.com/ and then copy you cookies and use it as the [value] of [key] \'cookies\' ")

        res = etree.HTML(resp.content)
        # get all pages
        # all_pages = res.xpath('//*[@id="pl_feedlist_index"]/div[3]/div[1]/span/ul/li//@href')
        items = res.xpath('//div[@class="card-wrap"]')
        df_list = []
        for i in items:
            try:
                content = i.xpath('.//div[@class="content"]//p//text()')
                content = ''.join(content)
                content = content.replace('\n', "")
                content = content.replace(' ', "")
                content = content.replace('\u200b', "")
            except:
                continue

            try:
                source = i.xpath('.//div[@class="from"]//a')
                date_content = source[0].text
                date_content = date_content.replace('\n', "")
                date_content = date_content.replace(' ', "")
                link = 'https:' + source[0].xpath('.//@href')[0].split('?')[0]
            except:
                date_content = np.nan
                link = None

            try:
                user = i.xpath('.//div[@class="content"]//p//@nick-name')[0]
            except:
                user = np.nan

            try:
                card_info = i.xpath(
                    './/div[@class="card-act"]//a[@class="woo-box-flex woo-box-alignCenter woo-box-justifyCenter"]')
                forward = ''.join(card_info[0].xpath('.//text()'))
                forward = forward.replace('\n', "")
                forward = forward.replace(' ', "")
                if not forward.isdecimal():
                    forward = 0
                comment = ''.join(card_info[1].xpath('.//text()'))
                comment = comment.replace('\n', "")
                comment = comment.replace(' ', "")
                if not comment.isdecimal():
                    comment = 0
                like = ''.join(card_info[2].xpath('.//text()'))
                like = like.replace('\n', "")
                like = like.replace(' ', "")
                if not like.isdecimal():
                    like = 0
            except:
                forward = np.nan
                comment = np.nan
                like = np.nan

            tmp = pd.DataFrame([date, date_content, user, content, link, forward, comment, like]).T
            tmp.columns = ["date", "date_content", "user", "content", "link", "forward", "comment", "like"]
            df_list.append(tmp)
        if df_list:
            self.dataframe = pd.concat([self.dataframe, pd.concat(df_list)])

        time.sleep(delay)
