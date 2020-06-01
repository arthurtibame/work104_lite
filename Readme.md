




 # 104 人力銀行 Crawler

## frontend 



 ## backend 
 
 ``` python
 url = "https://www.104.com.tw/jobs/search/?ro=0&keyword=data&area=6001001000%2C6002001000%2C6003001001&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc"
 ```
 
 
 keyword => 搜尋關鍵字

 area => 搜尋地區
    地區要爬出全部地區
    6001001001 <台灣, 台北市, 中正區>:
        6001 => 台灣
        001 =>台北
        000 => 全區
        001 =>中正區

    6001~6008        
 page => 搜尋出來頁數
    要做判斷 用while 直到不能跑
 mode => 模式 預設s
 jobsource=<year>indexpoc => 搜尋年分
    可以調 但預設為現在的年份

   

