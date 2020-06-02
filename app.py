from flask import Flask, render_template, request, redirect, url_for, flash, session
import re
import pandas as pd
from datetime import datetime

# setup the app
app = Flask(__name__)
app.config['DEBUG'] = True


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


    if request.method == 'GET':        
        return render_template('forms.html')
    

    if request.method =='POST':
        error_msg=None       
        keyword = request.form.get("keyword")
        country_id = int(request.form.get("country"))
        area_id = int(request.form.get("area_name"))
        set_create_datetime = datetime.now()
        create_date = str(set_create_datetime.date())
        create_time = str(set_create_datetime.time())[:-7] 
        print(area_id)
        if  keyword:
            
            df = pd.ExcelFile(r'./config/area_code.xlsx')
            country = df.sheet_names[country_id]
            area = df.parse(country).iloc[area_id, 1]
            newlog = [keyword, country, area, create_date, create_time]
            new_df = pd.DataFrame([newlog])
            new_df.to_csv(r'./config/logs.csv', mode="a" ,header=None, index=None, encoding="utf-8-sig")
      
      
            return render_template('forms.html')
        else:
            error_msgs = '請輸入關鍵字'
            return render_template('forms.html', error_msgs=error_msgs)
 


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