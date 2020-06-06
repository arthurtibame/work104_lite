import pandas as pd

class UserLogController(object):

    def __init__(self):
        try:
            LOG_PATH = r'./config/logs.csv'
            self.DF_LOG = pd.read_csv(LOG_PATH, encoding="utf-8-sig")
        except:
            self.DF_LOG = " "


        self.__df = self.__sepdf(self.DF_LOG)
        self.country = self.__duplicate_country
        self.keyword = self.__duplicate_keyword
        self.year = self.__duplcate_year
        self.month = self.__duplcate_month

    def __duplicate_country(self):
        return self.__df['country'].drop_duplicates().to_list()
        

    def __duplicate_keyword(self):
        return self.__df['keyowrd'].drop_duplicates().to_list()
        

    def __duplcate_area(self):
        return self.__df['area'].drop_duplicates().to_list()
        
    def __duplcate_year(self):
        return self.__df['create_year'].drop_duplicates().to_list()
        

    def __duplcate_month(self):
        return self.__df['create_year'].drop_duplicates().to_list()
        
    def __sepdf(self, *argu):
        """
        private function to initial dataframe which involve year month cols seperately
        """
        

        DF_LOG_LOCAL= self.DF_LOG
        a = [i for i in DF_LOG_LOCAL['create_date'].tolist()]
        DF_LOG_LOCAL['create_year'] = list(map(lambda x: self.__str2date(x).year, a))
        DF_LOG_LOCAL['create_month'] = list(
            map(lambda x: self.__str2date(x).month, a))
        return DF_LOG_LOCAL

    def __str2date(self, *argu):
        """
        Private function for  __sepdf to transfer from strdate 2 date type        
        """
        return datetime.strptime(*argu, '%Y-%m-%d')
        
