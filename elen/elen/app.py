from flask import Flask, render_template, request, redirect, url_for, flash, session, Response

import pandas as pd 
from sideprojects.work104.api.view_function import chk_folder_pages_counter, chk_folder_file
from sideprojects.work104.models.UserLogModel import UserLog, UserLogController, SearchUserLog
from sideprojects.work104.api import work104

app = Flask(__name__ , static_url_path='/static', static_folder='./static')
app.config['DEBUG'] = True
config_folder_path = r'./sideprojects/work104/config'
config_file_path = r'{}/logs.csv'.format(config_folder_path)


@app.route('/') #OK
def index():
    return render_template("index.html")

@app.route('/photography')
def photography():
    return render_template("photography.html")
@app.route('/sideproject')
def sideproject():
    return render_template("sideproject.html")
@app.route('/sideproject/work104', methods=["GET", "POST"])
def forms(): 
    
    global config_folder_path, config_file_path

    if request.method == 'GET':         
        return render_template('work104.html')            

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
            print(keyword, page, country_id, area_id)
            search_log = UserLog(keyword,country_id, area_id, page)
            search_log.create_log()

            #show logs
            df_history = pd.read_csv(r'./sideprojects/work104/config/logs.csv')
            df_history = df_history.to_dict(orient='records') 
            
            chk_folder_pages_counter()
            return render_template('work104_start_searching.html',\
                                    keyword=search_log.keyword, page=search_log.page,country=search_log.country, area=search_log.area)
        else: # show error msg and read history
            error_msgs = '必填'
            df_history = pd.read_csv(r'./sideprojects/work104/config/logs.csv')
            df_history = df_history.to_dict(orient='records') 
            return render_template('work104.html', error_msgs=error_msgs, df_history=df_history)
@app.route('/progress')
def progress():    
	return Response(work104.process_status(), mimetype= 'text/event-stream')
@app.route('/excution')
def excute():
    return work104.main()

@app.route('/travel') #OK
def travel():
    return render_template("travel.html")

@app.route('/fashion')#OK
def fashion():
    return render_template("fashion.html")

@app.route('/about') #OK
def about():
    return render_template("about.html")

@app.route('/contact') #OK
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
	# change to app.run(host="0.0.0.0"), if you want other machines to be able to reach the webserver.
	#app.run(port=8080, debug=True) 
    app.run(port=8080, debug=True)