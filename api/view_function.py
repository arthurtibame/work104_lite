import os
import pandas as pd

def chk_folder_file(folder_path, file_path):
        
        col_names = ["keyword", "country", "area", "area_code", "create_date", "create_time" ]
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