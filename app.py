from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
import re
import os
import pandas as pd
from datetime import datetime
from api import work104
from api.view_function import chk_folder_pages_counter, chk_folder_file
from time import sleep
from  models.UserLogModel import UserLog, UserLogController, SearchUserLog
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
            search_log = UserLog(keyword,country_id, area_id, page)
            search_log.create_log()

            #show logs
            df_history = pd.read_csv(r'./config/logs.csv')
            df_history = df_history.to_dict(orient='records') 
            
            chk_folder_pages_counter()
            return render_template('start_searching.html',\
                                    keyword=search_log.keyword, page=search_log.page,country=search_log.country, area=search_log.area)
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
    
def delete_history(path_file):
    try:
        return os.remove(path_file)
    except FileNotFoundError as e:
        return "0"


@app.route('/history', methods=["GET", "POST"])
def history():
    global config_file_path
    df = ""
    logs = UserLogController() 
    keywords = logs.keyword()
    countries = logs.country()
    areas = logs.area()
    years = logs.year()
    months = logs.month()
    if request.method == 'GET':  
        try:
            df = pd.read_csv(config_file_path)
            df = df.to_dict(orient='records')    
            return render_template('history.html', df=df, keywords=keywords, \
                countries=countries, areas=areas, years=years, months=months \
                )
        except:        
            return render_template('history.html', df=df, keywords=keywords, \
                countries=countries, areas=areas, years=years, months=months \
                )
    
    if request.method == "POST":
        try:
            delete = request.form.get("delete")       

            keyword = request.form.get("keyword")   
            country = request.form.get("country")   
            area = request.form.get("area")  
            print(keyword, country, area)
            df_search = SearchUserLog(keyword, country, area).search_result()               
            df_search = df_search.to_dict(orient='records')
            if delete is not None:
                delete_history(config_file_path)
                print("hi")
            if keyword or country or area:
                return render_template('history.html', df=df_search, keywords=keywords, \
                    countries=countries, areas=areas, years=years, months=months \
                    )
            
            return render_template('history.html', df=df, keywords=keywords, \
                countries=countries, areas=areas, years=years, months=months \
                )
        except:        
            return render_template('history.html', df=df, keywords=keywords, \
                countries=countries, areas=areas, years=years, months=months \
                )


if __name__ == "__main__":
	# change to app.run(host="0.0.0.0"), if you want other machines to be able to reach the webserver.
	#app.run(port=8080, debug=True) 
    app.run(host="0.0.0.0", port=8080, debug=True)
