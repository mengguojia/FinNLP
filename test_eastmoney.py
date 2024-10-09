from finnlp.data_sources.social_media.eastmoney_streaming import Eastmoney_Streaming

pages = 1000
end_date = '2024-10-08'
stock = "600519"
config = {
    "use_proxy": "china_free",
    "max_retry": 5,
    "proxy_pages": 8,
    }

downloader = Eastmoney_Streaming(config)
downloader.download_streaming_stock(stock, end_date, pages, delay=0.1)

print(downloader.dataframe.shape)

print(downloader.dataframe.head(1))
