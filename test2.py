from finnlp.data_sources.social_media.weibo_date_range import Weibo_Date_Range
#%%
start_date = "2024-01-01"
end_date = "2024-01-02"
stock = "茅台"
config = {
    "use_proxy": "china_free",
    "max_retry": 5,
    "proxy_pages": 4,
    "cookies": [{'SCF':'AgSKSNNF__c-jYUVZHHqzhwTg42PwMsvJuP3lgyg340N0ThFzkzJWqZUtSy1th6nn4Qc9Kp5dUBLATDUAtVUrMA.',
                 'SUB':'_2A25L5flMDeRhGeFH6loS8SfOzDSIHXVom3SErDV8PUNbmtANLRPkkW9Ne98MBWSNehprpMgFXeP7aNSeDYOyjWig',
                 'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9W59LmVM7.KqJ2caMVZSGlcV5JpX5KzhUgL.FoM4eKn0eK.ES0n2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1K2Re024eoMR',
                 'ALF':'02_1728648732'}],
}

#%%
downloader = Weibo_Date_Range(config)
downloader.download_date_range_stock(start_date, end_date, stock = stock)
df = downloader.dataframe
