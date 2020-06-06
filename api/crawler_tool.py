class JobContent:
    
    def __init__(self, json_content,job_code):
        self.basic_content = dict()
        self.json_content = json_content
        self.job_code = job_code       

    def job_basic_info(self):               
        try:
            self.basic_content['job_name'] = self.json_content['data']['header']['jobName']
        except:
            self.basic_content['job_name'] = r'職位名稱'
        
        try:
            self.basic_content['job_company'] = self.json_content['data']['header']['custName']
        except:
            self.basic_content['job_company'] = r'公司名稱'
        
        try:
            self.basic_content['job_requirement_Exp'] = self.json_content['data']['condition']['workExp']
        except:
            self.basic_content['job_requirement_Exp'] = r'無要求'
        
        try:
            self.basic_content['job_company_url'] = self.json_content['data']['header']['custUrl']        
        except:
            self.basic_content['job_company_url'] =  r"不詳"
        try:
            self.basic_content['job_code'] = f'https://www.104.com.tw/job/{self.job_code}?jobsource=jolist_b_relevance'
        except:
            self.basic_content['job_code']= r'不詳'

        return self.basic_content
    
    def job_basic_info_list(self):
        return list(self.job_basic_info().values())
    
    def job_description_list(self):
        
        description_list =list()
        # 抓出全部 decription
        try:
            for i in range(len(self.json_content['data']['condition']['specialty'])):
                
                job_detail = [self.json_content['data']['condition']['specialty'][i]['description'].lower()]
                
                if self.json_content['data']['condition']['specialty'][i]['description'] is None:
                    
                    print("++++++++++++++++++++++++++++++++++++++++++")
                    job_detail = ['無條件']                
                    description_list+=job_detail 
                description_list+=job_detail 
            if len(description_list) == 0 :
                description_list = ['無條件']   
            return description_list
        except:
            description_list = ['無條件']                      
            return description_list