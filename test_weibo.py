from finnlp.data_sources.social_media.weibo_date_range import Weibo_Date_Range
#%%
start_date = "2024-01-01"
end_date = "2024-01-02"
stock = "茅台"
config = {
    "use_proxy": "china_free",
    "max_retry": 5,
    "proxy_pages": 8,
    "cookies": ["XSRF-TOKEN=2lWIgDpoMKZTmpzOJnjrijmJ; SCF=AoDp1R6JLdrtLm1HRHrJOo550POoMLaPFTXdUntAcsSv8nnHpGrBmF7706p8f-JK1B9avIBzDV4OKZoDDGRCPUg.; SUB=_2A25L4vyBDeRhGeFH6loS8SfOzDSIHXVonnBJrDV8PUNbmtAGLVbakW9Ne98MBXrSF4mb6u3Jck3a0DS3LE5wh0D0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W59LmVM7.KqJ2caMVZSGlcV5JpX5KzhUgL.FoM4eKn0eK.ES0n2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1K2Re024eoMR; ALF=02_1728977362; WBPSESS=zIwU43xUakDnbfYNoOnwUfKhqClBj6PPAlCvRT5NIcWkof-MdGg5FmLQq_s9L_T5__pzjQz1_R0WxMKgwxcj-dnqeaNPGScBg3oAMDr2yD-Ecf2y2tTv1GeTvWRnWlUV",
                "SCF=AuWhXQ6zJw72tdZNYAQMK5mOtYXAsQ6lf8qQomIxj_ZjRxF5IT1OJU_q-1PzGhiDswjTVsw8ElrhQUwGBBxc0oE.; SUB=_2A25L76V2DeRhGeVM61UZ8yjIzj-IHXVohLi-rDV8PUNbmtAGLWGnkW9NTQsmEUUjv1a1-DO5RbLLckww0cC_CRt6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W55S4YENGhgWjGV3G_DMTi95JpX5KzhUgL.FoeEehMRe0qXSKe2dJLoIXnLxKqL1heLBoeLxKBLBonL12zLxKML1h2LB-zLxKML12zLBo2LxKML1-2L1hBLxK-L12BLBK2LxKnL12qLBozLxK-L12zL1Kzt; ALF=02_1729323559; Apache=9906046251011.582.1726731601844; SINAGLOBAL=9906046251011.582.1726731601844; ULV=1726731601847:1:1:1:9906046251011.582.1726731601844:"],
}

#%%
downloader = Weibo_Date_Range(config)
downloader.download_date_range_stock(start_date, end_date, stock = stock)
df = downloader.dataframe
