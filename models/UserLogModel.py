import pandas as pd
from datetime import datetime

AREA_CODE_PATH = r'./config/area_code.xlsx'
DF_AREA_DETAIL = pd.ExcelFile(AREA_CODE_PATH)
CREATE_TIME = datetime.now()
try:
    LOG_PATH = r'./config/logs.csv'
    DF_LOG = pd.read_csv(LOG_PATH, encoding="utf-8-sig")
except:
    DF_LOG= " "  

class UserLog(object):
    """
    讓使用者建立 一筆log
    """

    def __init__(self, keyword, country_id, area_id ,page):
        """
        initialize country,area from country_id, area_id which is got from 'area_code.xlsx'        
        """
        global DF_LOG, DF_AREA_DETAIL, CREATE_TIME      
        
        self.keyword = str(keyword)        
        self.country = DF_AREA_DETAIL.sheet_names[country_id]
        self.area = DF_AREA_DETAIL.parse(self.country).iloc[area_id, 1]
        self.area_code = DF_AREA_DETAIL.parse(self.country).iloc[area_id, 2]
        self.page = page
        self.create_date = str(CREATE_TIME.date())
        self.create_time = str(CREATE_TIME.time())[:-7] 
        
    def create_log(self):
        """
        Let user create data in logs.csv
        """
        NEWLOG_LIST = [self.keyword, self.country, self.area, self.area_code, self.page, self.create_date, self.create_time]
        NEW_DF = pd.DataFrame([NEWLOG_LIST])
        
        NEW_DF.to_csv(r'./config/logs.csv', mode="a" ,header=None, index=None, encoding="utf-8-sig")
    

class SearchUserLog(object):
    
    def __init__(self, keyword, country, area, year, month):
        
        global LOG_PATH, DF_LOG
        
        self.keyword = keyword
        self.country = country
        self.area = area
        self.year = year
        self.month = month        
        self.df = self.__sepdf(DF_LOG) #dealwith sep month
        
    def search_result(self):
        MY_FILTER = self.df[(self.df['keyword']==self.keyword) & (self.df['country']==self.country) &\
            (self.df['area']==self.area) & (self.df['create_year']==self.year) & (self.df['create_month']==self.month)]
        MY_FILTER_DF = MY_FILTER[['keyword', 'country', 'area', 'create_date' ]]
        return MY_FILTER_DF    
    def delete_log(self):
        MY_FILTER = self.df[(self.df['keyword']==self.keyword) & (self.df['country']==self.country) &\
            (self.df['area']==self.area) & (self.df['create_year']==self.year) & (self.df['create_month']==self.month)]
    
    def __sepdf(self, df):
        """
        private function to initial dataframe which involve year month cols seperately
        """
        global DF_LOG

        a = [i for i in DF_LOG['create_date'].tolist()]
        DF_LOG['create_year'] = list(map(lambda x: self.__str2date(x).year,a))
        DF_LOG['create_month'] = list(map(lambda x: self.__str2date(x).month,a))
        return df
    
    def __str2date(self, date_time_str):    
        """
        Private function for  __sepdf to transfer from strdate 2 date type        
        """
        DATE = datetime.strptime(date_time_str, '%Y-%m-%d')
        return DATE

if __name__ == "__main__":
    
    a = SearchUserLog(keyword="data analyst", country="Taiwan", \
                    area="台北市", year=2020, month=6).search_result()
    print(a)

