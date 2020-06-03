from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
import re
import os
import pandas as pd
import threading
from datetime import datetime
from api import work104, view_function
from api.view_function import chk_folder_pages_counter
from time import sleep

# setup the app
app = Flask(__name__)
app.config['DEBUG'] = True
config_folder_path = r'./config'
config_file_path = r'{}/logs.csv'.format(config_folder_path)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/tables')
def tables():

    return render_template('tables.html')


@app.route('/forms', methods=["GET", "POST"])
def forms(): 
    
    global config_folder_path, config_file_path

    if request.method == 'GET':  
        
        chk = view_function.chk_folder_file(config_folder_path, config_file_path)
        df_history = pd.read_csv(config_file_path)
        df_history = df_history.to_dict(orient='records')
        return render_template('forms.html',df_history=df_history)            

    if request.method =='POST':        
        
        view_function.chk_folder_file(config_folder_path, config_file_path)
        df_history = pd.read_csv(config_file_path)
        df_history = df_history.to_dict(orient='records')        
        # get logs
        error_msgs=None       
        keyword = request.form.get("keyword")        
        
        if  keyword: # If got keyword save log
            
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
            newlog = [keyword, country, area, area_code, create_date, create_time]
            new_df = pd.DataFrame([newlog])
            # 判斷有沒有檔案

            new_df.to_csv(r'./config/logs.csv', mode="a" ,header=None, index=None, encoding="utf-8-sig")
            #save 

            # and show logs
            df_history = pd.read_csv(r'./config/logs.csv')
            df_history = df_history.to_dict(orient='records') 
            
            chk_folder_pages_counter()
            return render_template('start_searching.html',keyword=keyword, country=country, area=area)
        else: # show error msg and read history

            error_msgs = '必填'
            df_history = pd.read_csv(r'./config/logs.csv')
            df_history = df_history.to_dict(orient='records') 
            return render_template('forms.html', error_msgs=error_msgs, df_history=df_history)

#@app.route('/progress')
#def progress():
#    def generate():



@app.route('/progress')
def progress():    
	return Response(work104.process_status(), mimetype= 'text/event-stream')

@app.route('/excution')
def excute():
    return work104.main()

@app.route('/bootstrap-elements')
def bootstrap_elements():
    return render_template('bootstrap-elements.html')

@app.route('/bootstrap-grid')
def bootstrap_grid():
    return render_template('bootstrap-grid.html')

@app.route('/history')
def history():
    df = ""
    try:
        df = pd.read_csv(r'./config/logs.csv')
        df = df.to_dict(orient='records')
        return render_template('history.html', df=df)
    except:        
        return render_template('history.html', df=df)

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == "__main__":
	# change to app.run(host="0.0.0.0"), if you want other machines to be able to reach the webserver.
	app.run(port=8080, debug=True) 