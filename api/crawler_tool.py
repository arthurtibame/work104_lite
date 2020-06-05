class JobContent:
    
    def __init__(self, json_content,job_code):
        self.basic_content = dict()
        self.json_content = json_content
        self.job_code = job_code       

    def job_basic_info(self):               
        
        self.basic_content['job_name'] = self.json_content['data']['header']['jobName']
        self.basic_content['job_company'] = self.json_content['data']['header']['custName']
        self.basic_content['job_requirement_Exp'] = self.json_content['data']['condition']['workExp']
        self.basic_content['job_company_url'] = self.json_content['data']['header']['custUrl']        
        self.basic_content['job_code'] = f'https://www.104.com.tw/job/{self.job_code}?jobsource=jolist_b_relevance'
        
        return self.basic_content
    
    def job_basic_info_list(self):
        return list(self.job_basic_info().values())
    
    def job_description(self):
        
        job_description_list =list()
        # 抓出全部 decription
        for i in range(len(self.json_content['data']['condition']['specialty'])):
            
            job_detail = [self.json_content['data']['condition']['specialty'][i]['description']]
            if len(job_detail)==0:
                job_detail = ['無條件']                
            job_description_list+=job_detail 

        return job_description_list