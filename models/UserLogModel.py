import pandas as pd
from datetime import datetime

LOG_PATH = r'./config/logs.csv'
AREA_CODE_PATH = r'./config/area_code.xlsx'
DF_AREA_DETAIL = pd.ExcelFile(AREA_CODE_PATH)
CREATE_TIME = datetime.now()
 

class UserLog(object):
    """
    讓使用者建立 一筆log
    """

    def __init__(self, keyword, country_id, area_id ,page):
        """
        initialize country,area from country_id, area_id which is got from 'area_code.xlsx'        
        """
        global DF_AREA_DETAIL, CREATE_TIME      
        
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
       
    def __init__(self, keyword, country, area):
        
        global LOG_PATH
        try:            
            self.DF_LOG = pd.read_csv(LOG_PATH, encoding="utf-8-sig")
        except:
            self.DF_LOG= " " 
        
        self.keyword = keyword
        self.country = country
        self.area = area
        self.df = self.__sepdf(self.DF_LOG) #dealwith sep month
        
    def search_result(self):


        MY_FILTER = self.__search_switcher(1)
        MY_FILTER_DF = MY_FILTER[['keyword', 'country', 'area', 'create_date', 'create_time' ]]
        return MY_FILTER_DF    

    def delete_log(self):

        MY_FILTER = self.df[(self.df['keyword']==self.keyword) & (self.df['country']==self.country) &\
            (self.df['area']==self.area)]

    def __search_switcher(self, i):
    
        switcher = {
            1: self.df[(self.df['keyword']==self.keyword)],
            
            2: self.df[(self.df['country']==self.country)],
            
            3: self.df[(self.df['area']==self.area)],
            
            4: self.df[(self.df['keyword']==self.keyword) & (self.df['country']==self.country)],
            
            5: self.df[(self.df['keyword']==self.keyword) & (self.df['area']==self.area)],              
            
            6: self.df[(self.df['country']==self.country) & (self.df['area']==self.area)],
            
            7: self.df[(self.df['keyword']==self.keyword) & (self.df['country']==self.country) &\
                (self.df['area']==self.area)],                
        }
        return switcher.get(i)
    
    
    def __sepdf(self, df):
        """
        private function to initial dataframe which involve year month cols seperately
        """
        a = [i for i in self.DF_LOG['create_date'].tolist()]
        self.DF_LOG['create_year'] = list(map(lambda x: self.__str2date(x).year,a))
        self.DF_LOG['create_month'] = list(map(lambda x: self.__str2date(x).month,a))
        return df
    
    def __str2date(self, date_time_str):    
        """
        Private function for  __sepdf to transfer from strdate 2 date type        
        """
        DATE = datetime.strptime(date_time_str, '%Y-%m-%d')
        return DATE

class UserLogController(object):

    def __init__(self):
        global LOG_PATH 
        try:            
            self.DF_LOG = pd.read_csv(LOG_PATH, encoding="utf-8-sig")
        except:
            self.DF_LOG= " " 
        self.__df = self.__sepdf()
        self.country = self.__duplicate_country
        self.keyword = self.__duplicate_keyword
        self.area = self.__duplcate_area
        self.year = self.__duplcate_year
        self.month = self.__duplcate_month
    
    def __add_all2_list(self, list_):
        return list_.insert(0, "全部")
    def __duplicate_country(self):
        try:
            COUNTRY = self.__df['country'].drop_duplicates().to_list()
            self.__add_all2_list(COUNTRY)
            return COUNTRY
        except:
            return ["none"]       

    def __duplicate_keyword(self):
        try:
            KEYWORD = self.__df['keyword'].drop_duplicates().to_list()
            self.__add_all2_list(KEYWORD)
            return KEYWORD
        except:
            return ["none"]       

    def __duplcate_area(self):
        try:
            AREA = self.__df['area'].drop_duplicates().to_list()
            self.__add_all2_list(AREA)
            return AREA
        except:
            return ["none"]       
        
    def __duplcate_year(self):
        try:
            YEAR = self.__df['year'].drop_duplicates().to_list()
            self.__add_all2_list(YEAR)
            return YEAR
        except:
            return ["none"]       

    def __duplcate_month(self):
        try:
            MONTH = self.__df['month'].drop_duplicates().to_list()
            self.__add_all2_list(MONTH)
            return MONTH
        except:
            return ["none"]       
        
    def __sepdf(self):
        """
        private function to initial dataframe which involve year month cols seperately
        """
        try:
            DF_LOG_LOCAL= self.DF_LOG
            a = [i for i in DF_LOG_LOCAL['create_date'].tolist()]
            DF_LOG_LOCAL['create_year'] = list(map(lambda x: self.__str2date(x).year, a))
            DF_LOG_LOCAL['create_month'] = list(
                map(lambda x: self.__str2date(x).month, a))
            return DF_LOG_LOCAL
        except:
            return "No data"

    def __str2date(self, x):
        """
        Private function for  __sepdf to transfer from strdate 2 date type        
        """
        return datetime.strptime(x, '%Y-%m-%d')

if __name__ == "__main__":
    
    a = SearchUserLog(keyword="data analyst", country="Taiwan", \
                    area="台北市", year=2020, month=6).search_result()
    print(a)

