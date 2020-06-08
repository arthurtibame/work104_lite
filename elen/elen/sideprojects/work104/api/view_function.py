import os
import pandas as pd
import shutil

pages_counter_path = r'./sideprojects/work104/pages_counter/'

def chk_folder_file(folder_path, file_path):
        
        col_names = ["keyword", "country", "area", "area_code","page", "create_date", "create_time","id" ]
        df_temp = pd.DataFrame(columns=[col_name for col_name in col_names])
        
        if os.path.isdir(folder_path) is False:
            os.mkdir(folder_path)        
            df_temp.to_csv(file_path,index=None,encoding='utf-8-sig')
            
        elif os.path.isfile(file_path) is False : # file is not exist
            df_temp.to_csv(file_path,index=None,encoding='utf-8-sig')
            
        else:
            df = pd.read_csv(file_path)
            if df.columns.tolist() != col_names:
                df_temp.to_csv(file_path,index=None,encoding='utf-8-sig')   
                
        return "1"

def chk_folder_pages_counter():
        
        # 檢查dir 
        if os.path.isdir(pages_counter_path) is False:
            os.mkdir(pages_counter_path)        
        else:
            shutil.rmtree(pages_counter_path)
            os.mkdir(pages_counter_path)        
        return 'done'


