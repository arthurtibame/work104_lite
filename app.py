from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
import re
import os
import pandas as pd
from datetime import datetime
from api import work104
from api.view_function import chk_folder_pages_counter, chk_folder_file
from time import sleep

# setup the app
app = Flask(__name__)
app.config['DEBUG'] = True
config_folder_path = r'./config'
config_file_path = r'{}/logs.csv'.format(config_folder_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forms', methods=["GET", "POST"])
def forms(): 
    
    global config_folder_path, config_file_path

    if request.method == 'GET':  
        
        chk_folder_file(config_folder_path, config_file_path)
        df_history = pd.read_csv(config_file_path)
        df_history = df_history.to_dict(orient='records')
        return render_template('forms.html',df_history=df_history)            

    if request.method =='POST':        
        
        chk_folder_file(config_folder_path, config_file_path)
        df_history = pd.read_csv(config_file_path)
        df_history = df_history.to_dict(orient='records')        
        # get logs
        error_msgs=None       
        keyword = request.form.get("keyword")
        page = request.form.get("page")
        
        if  keyword and page: # If got keyword save log
            
            country_id = int(request.form.get("country"))
            area_id = int(request.form.get("area_name"))

            set_create_datetime = datetime.now()
            create_date = str(set_create_datetime.date())
            create_time = str(set_create_datetime.time())[:-7] 

            df = pd.ExcelFile(r'./config/area_code.xlsx')
            country = df.sheet_names[country_id]
            area = df.parse(country).iloc[area_id, 1]
            area_code = df.parse(country).iloc[area_id, 2]

            #save logs
            newlog = [keyword, country, area, area_code, page, create_date, create_time]
            new_df = pd.DataFrame([newlog])
            
            new_df.to_csv(r'./config/logs.csv', mode="a" ,header=None, index=None, encoding="utf-8-sig")
            

            #show logs
            df_history = pd.read_csv(r'./config/logs.csv')
            df_history = df_history.to_dict(orient='records') 
            
            chk_folder_pages_counter()
            return render_template('start_searching.html',keyword=keyword, page=page,country=country, area=area)
        else: # show error msg and read history

            error_msgs = '必填'
            df_history = pd.read_csv(r'./config/logs.csv')
            df_history = df_history.to_dict(orient='records') 
            return render_template('forms.html', error_msgs=error_msgs, df_history=df_history)

@app.route('/progress')
def progress():    
	return Response(work104.process_status(), mimetype= 'text/event-stream')
@app.route('/excution')
def excute():
    return work104.main()
@app.route('/history')
def history():
    df = ""
    try:
        df = pd.read_csv(r'./config/logs.csv')
        df = df.to_dict(orient='records')
        return render_template('history.html', df=df)
    except:        
        return render_template('history.html', df=df)

if __name__ == "__main__":
	# change to app.run(host="0.0.0.0"), if you want other machines to be able to reach the webserver.
	#app.run(port=8080, debug=True) 
    app.run(host="0.0.0.0", port=8080, debug=True)