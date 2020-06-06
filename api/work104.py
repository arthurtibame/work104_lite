import requests
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime
import os
import json
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError
from api.crawler_tool import JobContent # 如果從 app用這個
#from crawler_tool import JobContent # 如果從這裡開改這個     
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'
           }
pages_amount_path = r'./pages_counter/.pages_amount.txt'
pages_count_path = r'./pages_counter/.pages_count.txt'
str_date = datetime.now().strftime("%Y%m%d")
result_code = list() 
final_list = list()
job_requirements_counter = 0 # to count the number of requirements in DataFrame
detail_crawler_count = 0 # control now detail page
now_page = 1 # control result urls' pages
main_status_code = 0

def requests_get(*args1, **args2):
    i = 3
    while i >= 0:
        try:
            return requests.get(*args1, **args2)
        except (ConnectionError, ReadTimeout) as error:
            print(error)
            print('retry one more time after 60s', i, 'times left')
            sleep(60)
        i -= 1
    return pd.DataFrame()

def chk_folder_pages_counter():
    path = r'./pages_counter/'
    # 檢查dir 
    if os.path.isdir(path) is False:
        os.mkdir(path)        
    else:
        os.removedirs(path)
        os.mkdir(path)

    return 'done'

def get_result_urls(keyword, area_code=None, require_amount_pages=None):
    '''
    keyword 使用者必填
    job_year 預設現在年分
    area 預設全台灣
    page 預設第一頁
    '''    
    print(require_amount_pages)
    global now_page

    while True:
        payload = {}
        payload["keyword"] = keyword
        payload["area_code"] = area_code
        payload["page"] = str(now_page)
        payload["job_year"] = str(datetime.now().year)

        
        if payload["area_code"]:
            url = "https://www.104.com.tw/jobs/search/?ro=0&keyword={}&area={}&order=15&asc=0&page={}&mode=s&jobsource={}indexpoc"\
                .format(payload["keyword"], payload["area_code"], payload["page"], payload["job_year"])
        else:
            url = "https://www.104.com.tw/jobs/search/?ro=0&keyword={}&order=15&asc=0&page={}&mode=s&jobsource={}indexpoc"\
                .format(payload["keyword"], payload["page"], payload["job_year"])
        
        global headers
    
        try:
            res = requests.get(url, headers)
            soup = BeautifulSoup(res.text, "html.parser")
            job_content = soup.select("article")
            title = soup.select('div[class="b-block__left"] h2[class="b-tit"] a')
            
            # check pages is it the final page
            if len(title) == 0:                    
                break            
        except:
            print('Error of [get_result_urls]', "Page {}".format(now_page), url)
            print('Try Again after sleep 10 seconds !')
            sleep(10)
            continue
        print("")
        print("===============page {}".format(now_page))
        for job_urls in job_content:
            if job_urls:
                try:                    
                    job_code = job_urls.a['href'][21:26]               
                    result_code.append(job_code)
                    print("Got job code: {}".format(job_code))      

                except:
                    continue
        if require_amount_pages and require_amount_pages==now_page:
            break
        now_page+=1

        
def crawl_detail(keyword, job_code, country, area_name):    
    # check file dir if not exist create it

    
    # insert Referer to crawl details
    global headers, job_requirements_counter, final_list, detail_crawler_count, str_date

    headers["Referer"] = "https://www.104.com.tw/job/{}".format(job_code)
    try: 
        url = "https://www.104.com.tw/job/ajax/content/{}".format(job_code)
        res = requests_get(url, headers=headers)
        json_content = json.loads(res.text)       
        
    except:
        return 0
        
    data_dir = r'./data'
    data_path = f'{data_dir}/{country}' 
    area_path = f'{data_path}/{area_name}'
    keyword_path = f'{area_path}/{keyword}'
    try:        
        os.mkdir(data_dir)
    except:
        pass    
    try:        
        os.mkdir(data_path)
    except:
        pass    
    try:
        os.mkdir(area_path)
    except:
        pass
    try:   
        os.mkdir(keyword_path)
    except:
        pass

    
    str_date = datetime.now().strftime("%Y%m%d")     
    detail_crawler_count+=1
    
    # get basic info of the job -> call job content
    job_content = JobContent(json_content,job_code)
    job_basic_content = job_content.job_basic_info_list()
    job_description = job_content.job_description_list()

    df_description = pd.DataFrame([job_description])
    df_description.to_csv(f"{keyword_path}/mapreduce.csv",mode='a', index=None, header=False,encoding="utf-8-sig")

    ## 處理else !
    basic_col_names = ['職位名稱', '公司名稱','工作經歷','公司連結', '職位連結'] 
    if detail_crawler_count == 1: # if first loop add col names        
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++ first loop")
        df = pd.DataFrame([job_basic_content], columns=basic_col_names)
        df.to_csv(f"{keyword_path}/{str_date}.csv",mode='a', index=None,encoding="utf-8-sig")    
    elif detail_crawler_count> 1 : 
        df_exist = pd.read_csv(f"{keyword_path}/{str_date}.csv",encoding="utf-8-sig")
        df_new = pd.DataFrame([job_basic_content], columns=basic_col_names)
        df_new = pd.concat([df_exist, df_new])
        df_new.to_csv(f"{keyword_path}/{str_date}.csv", index=None,encoding="utf-8-sig")    
    
def process_status():
    global pages_amount_path, pages_count_path, detail_crawler_count, result_code, main_status_code, final_list, job_requirements_counter,now_page
    
    try:
        if main_status_code==1:
            print("因為篩選有刪除資料所以判斷 main_status_code\
                    不然百分比沒辦法 match\
                ")
            main_status_code=0
            result_code = list() 
            final_list = list()
            job_requirements_counter = 0 # to count the number of requirements in DataFrame
            detail_crawler_count = 0 # control now detail page
            now_page = 1 # control result urls' pages
            
        while os.path.isfile(pages_amount_path) == True:
            
            one_percent_page_amount = len(result_code)/100   
            
            now_percent = 0
            while now_percent <= 100:
                if main_status_code == 1:
                    main_status_code=0
                    result_code = list() 
                    final_list = list()
                    job_requirements_counter = 0 # to count the number of requirements in DataFrame
                    detail_crawler_count = 0 # control now detail page
                    now_page = 1 # control result urls' pages                    
                    yield "data:" + str(100) + "\n\n"
                    print("目前進度: {} %".format(100))
                    break
                now_percent = round(detail_crawler_count/one_percent_page_amount,2)
                print("=========================")
                print("目前進度: {} %".format(now_percent))
                yield "data:" + str(now_percent) + "\n\n"
                
                sleep(0.5)
            break
    except ZeroDivisionError as e:
        yield "data:" + str(100) + "\n\n"
        print(e)

        
def read_latest_log():
    
    df = pd.read_csv(r'./config/logs.csv')
    keyword = df.iloc[len(df)-1,0]
    area_code = df.iloc[len(df)-1,3]
    page = df.iloc[len(df)-1,4]
    country = df.iloc[len(df)-1, 1]
    area_name = df.iloc[len(df)-1, 2]

    search_index = [str(keyword), int(area_code), int(page), str(country), str(area_name)]

    return search_index

def chk_all_description(keyword, modify_csv_path):
    """
    1. 上面<crawl_detail function>建立一個 mapreduce.csv每行分別為每筆資料的技能要求
    2. 處理 mapreduce.csv 令一個list變數 去接 -> 重複值篩選掉、留下不重複的技能要求
    3. 第2點令的list 去比對每一行 若有給1沒有為0
    4. 利用pandas.concat 合併
    """
    import itertools
    
    mapreduce_csv_path = f'{modify_csv_path}/mapreduce.csv'
    df = pd.read_csv(f'{mapreduce_csv_path}', sep='delimiter', header=None, encoding='utf-8-sig')
    df_list = df.iloc[:,0].tolist()
    list_of_list_description = [x.split(',') for x in df_list]
    all_description_list = list(map(lambda x: x.replace('\u200b',''),list(dict.fromkeys(list(itertools.chain.from_iterable([x.split(',') for x in df.iloc[:,0].tolist()]))))))
    result_list = list()
    for not_import_index ,each_description_list in enumerate(list_of_list_description):
        tmp_list = list()
        for i in range(len(all_description_list)):
            if all_description_list[i] not in each_description_list:
                tmp_list.append(0)
            else :
                tmp_list.append(1)
        result_list.append(tmp_list)    

    df_result = pd.DataFrame(result_list,columns=all_description_list)
    df_result = df_result.drop(columns=['無條件'])
    #df_result.to_csv(mapreduce_csv_path,index=None, encoding='utf-8-sig')

    global str_date
    save_path = f'{modify_csv_path}/{str_date}.csv'
    df1 = pd.read_csv(save_path,encoding='utf-8-sig')
    df_final = pd.concat([df1, df_result], axis=1)
    df_final.to_csv(save_path,index=None,encoding='utf-8-sig')
    os.remove(mapreduce_csv_path)


def main():  
    global main_status_code, now_page, pages_amount_path, pages_count_path, str_date
    
    # 設定起始時間
    start_time = datetime.now()      
    # 讀取參數 area code + keyword
    sleep(1.5) # wait for user save
    search_index = read_latest_log() # type -> list
    # 抓資料筆數
    if search_index[2] != 0:
   
        get_result_urls(search_index[0], search_index[1], search_index[2])        
    else:
        get_result_urls(search_index[0], search_index[1])       # 找全部頁面面
    #chk folder
    with open(pages_amount_path, 'w') as f:
        f.write(str(now_page))
    with open(pages_count_path, 'w') as f:
        f.write('0')
    # start crawl detail page
    for i in result_code:
        crawl_detail(search_index[0], i, search_index[-2], search_index[-1])    

    # map the job decription
    modify_csv_path = f'./data/{search_index[-2]}/{search_index[-1]}/{search_index[0]}'
    chk_all_description(search_index[0], modify_csv_path)
    
    # 設定結束時間並回傳
    end_time = datetime.now()
    used_time = (end_time - start_time).seconds
    global main_status_code
    main_status_code += 1
    print(used_time)   
    
    if used_time >=5:
        return """<p style='font-size:20px; color:green;'>&#9989; 使用了 {} 秒完成</p>
                
                """.format(used_time)
    else:
        return """<p style='font-size:20px; color:red;'>&#10060; 請檢查檔案! 只使用了 {} 秒完成</p>
                
                """.format(used_time)

if __name__ == "__main__":
    
    #get_result_urls('data')#,require_amount_pages=2)
    
    crawl_detail('data','6iz90')

#    for i in result_code:
#        crawl_detail('data',str(i))
    
