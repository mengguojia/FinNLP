from finnlp.data_sources.news.sina_finance_date_range import Sina_Finance_Date_Range

start_date = "2024-06-01"
end_date = "2024-06-05"
config = {
    "use_proxy": "china_free",
    "max_retry": 5,
    "proxy_pages": 5,
}

news_downloader = Sina_Finance_Date_Range(config)
news_downloader.download_date_range_all(start_date,end_date)
news_downloader.gather_content()