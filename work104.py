import requests
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime
import os
import json
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'
           }

result_code = list() 
final_list = list()
job_requirements_counter = 0 # to count the number of requirements in DataFrame
save_csv_times = 0
def tackle_area(area="All", country="Taiwan"):
    """
    1. Choose SHEET NAME by country(must be EN): Taiwan, China, Asia, Australia, America, South_America, Europe, Afica 
    2. Choose AREA NAME by English or Chinese
        - distinguish chinese, english
            * link = https://www.twblogs.net/a/5d6d0176bd9eee5327ff0641
    3. return AREA CODE in this function 
    """
    try:
        if all(map(lambda c:'\u4e00' <= c <= '\u9fa5',area)) == True:    
            #print('input is {} Chinese'.format(area))
            col_name = 'Area_zh_tw'
        else:
            #print('input is NOT {} Chinese'.format(area))
            col_name = 'Area_en'

        df = pd.read_excel(open(r"./area_code.xlsx", 'rb'),sheet_name=country)
        df_choose = df.loc[df[col_name] == area]
        area_code = df_choose.iloc[0,2]
        return area_code
    except:
        print("Error: [tackle_area] ")
        return 0

def get_result_urls(keyword, job_year, area_code=None):
    '''
    keyword 使用者必填
    job_year 預設現在年分
    area 預設全台灣
    page 預設第一頁
    '''
    now_page = 1
    while True:
        payload = {}
        payload["keyword"] = keyword
        payload["area_code"] = area_code
        payload["page"] = str(now_page)
        payload["job_year"] = job_year

        
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
        now_page+=1
    # check len of result_urls          
    if len(result_code) != 0:
        return len(result_code)
    else:
        return None
        
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


def crawl_detail(keyword, job_code):
    
    def job_requirements_filter(job_requirements=[]):
        
        final_list=list()
        for i in range(len(job_requirements)):
            k = job_requirements[i][0]
            try:
                if int(k) and i < 10:
                    final = job_requirements[i][2:]
                    final_list.append(final)
                elif int(k) and i>=10:
                    final = job_requirements[i][3:]
                    final_list.append(final)
            except:
                pass
        return final_list
    # check file
    data_path = r'./data'
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    
    # insert Referer to crawl details
    global headers, job_requirements_counter, final_list
    headers["Referer"] = "https://www.104.com.tw/job/{}".format(job_code)
    try: 
        url = "https://www.104.com.tw/job/ajax/content/{}".format(job_code)
        res = requests_get(url, headers=headers)
        json_content = json.loads(res.text)
    except:
        return 0

    # create a tmp list 
    tmp_list = list()
    try:
        job_name = [json_content['data']['header']['jobName']]
    except:
        pass
    try:            
        job_company = [json_content['data']['header']['custName']]
    except:
        pass
    try:
        job_company_url = [json_content['data']['header']['custUrl']]
    except:
        pass
    try:
        job_requirement_Exp = [json_content['data']['condition']['workExp']]
    except:
        pass
    try:
        job_requirements_tmp =json_content['data']['condition']['other'].replace('  ','').replace('\t','').replace('\r','').replace(',','').replace('•','').split('\n')[:]
        job_requirements_tmp = [i for i in job_requirements_tmp if len(i)>1]
        job_requirements = job_requirements_filter(job_requirements_tmp)
        len_job_requirements = len(job_requirements)
        
        if job_requirements_counter < len_job_requirements:
            job_requirements_counter = len_job_requirements
    except:
        pass
    if len(job_requirements) > 1:
        tmp_list = job_name + job_company + job_company_url + job_requirement_Exp + job_requirements
        final_list.append(tmp_list)
        df = pd.DataFrame(final_list) # ,columns=["職缺", "公司名稱", "公司簡介url", "工作經歷", "所需技能"]
        str_date = datetime.now().strftime("%Y%m%d")
        
        global save_csv_times
        
        data_path = r'./data/{}'.format(keyword)
        if not os.path.isdir(data_path):
            os.mkdir(data_path)
        if save_csv_times ==0:
            df.to_csv(r"{}/{}{}.csv".format(data_path,keyword, str_date),mode='a', index=None,encoding="utf-8-sig")
            save_csv_times+=1
        else:
            df.to_csv(r"{}/{}{}.csv".format(data_path,keyword, str_date),mode='a', header=False, index=None,encoding="utf-8-sig")
            save_csv_times+=1    

def work_crawler(keyword, area="All", country="Taiwan", job_year=str(date.today().year)):    
    start_time = datetime.now()
    if area=="All" and country=="Taiwan":
        get_result_urls(keyword,job_year=job_year)
    
    else:
        area_code = tackle_area(area=area, country=country)
        if area_code != 0:
            get_result_urls(keyword= keyword,area_code=area_code, job_year=job_year)
    for i in result_code:
        crawl_detail(keyword, i)
    
    end_time = datetime.now()
    used_time = (end_time - start_time).seconds
    if used_time == 0:
        return 'Please check the country or area'
    else:
        return used_time
if __name__ == "__main__":
    a = work_crawler("data", area="Taoyuan",country="Taiwan",job_year=2019)
    print(a)

