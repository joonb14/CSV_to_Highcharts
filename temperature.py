#from flask import render_template
from flask import Flask, request, render_template, send_from_directory, url_for
import matplotlib.pyplot as plt
import os
from werkzeug import secure_filename
import io
import base64
from cycler import cycler
import datetime
import matplotlib.dates as mdates
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib import style
import time
import pandas as pd
import numpy as np
import glob

UPLOAD_FOLDER = os.path.basename('plots')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():

    #img = io.BytesIO()

    style.use('fivethirtyeight')
    #plt.clear() # to wipe data and redraw! maybe wasting resource
    fig = plt.figure(figsize=(7,5),tight_layout=True) # figsize=(x,y)
    plt.xticks(rotation=270)
    fig.suptitle('iBeacon Temperature', fontsize=20)
    plt.xlabel('Datetime', fontsize=18)
    plt.ylabel('Temperature', fontsize=16)

    files = glob.glob("*-*-*_*-*-*.csv")
    df=pd.read_csv(files[0], names=['Name','UUID','Major','Minor','formattedtime','time','temperature','humidity','rssi','data'])
    #일단은 5개의 색으로 충분하다고 가정
    color_list=['red','blue','green','yellow','black']
    color_index = 0
    major_type = df.Major.unique()
    major_label=[]
    for major in major_type:
        if major > 10: continue
            #since if major is over 10 its not the packet to watch for Temperature
        xs=[]
        ys=[]
        for index, row in df.iterrows():
            if(row['Major']==major):
                x = _convert_java_millis(row['time'])
                y = row['temperature']
                xs.append(x)
                ys.append(y)
        #fig.autofmt_xdate()
        plt.plot(xs, ys,color=color_list[color_index],linewidth=1.0, antialiased=True)
        color_index+=1
        major_label.append("Major : " + str(major))

    plt.legend(major_label,loc='upper right')
    
    #WARNING: QApplication was not created in the main() thread.
    #이라는 에러가 계속 남 
    #ani = animation.FuncAnimation(fig=fig, func=animate, interval=1000) # 1000ms = 1sec
    filename = "temperature.png"
    f = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    plt.savefig(f, format='png')
    #img.seek(0)

    #plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html',filename=filename)


def _convert_java_millis(java_time_millis):
    """Provided a java timestamp convert it into python date time object"""
    ds = datetime.datetime.fromtimestamp(
        int(str(java_time_millis)[:10])) if java_time_millis else None
    ds = ds.replace(hour=ds.hour,minute=ds.minute,second=ds.second,microsecond=int(str(java_time_millis)[10:]) * 1000)
    return ds


def animate(i):
    # pattern *-*-*_*-*-*.csv
    # ex) 2018-07-23_14-19-34.csv
    files = glob.glob("*-*-*_*-*-*.csv")
    df=pd.read_csv(files[0], names=['Name','UUID','Major','Minor','formattedtime','time','temperature','humidity','rssi','data'])
    color_list=['red','blue','green','yellow','black']
    color_index = 0
    major_type = df.Major.unique()
    major_label=[]
    for major in major_type:
        if major > 10: continue
            #since if major is over 10 its not the packet to watch for Temperature
        xs=[]
        ys=[]
        for index, row in df.iterrows():
            if(row['Major']==major):
                x = _convert_java_millis(row['time'])
                y = row['temperature']
                xs.append(x)
                ys.append(y)
        #fig.autofmt_xdate()
        plt.plot(xs, ys,color=color_list[color_index],linewidth=1.0, antialiased=True)
        color_index+=1
        major_label.append("Major : " + str(major))

    plt.legend(major_label,loc='upper right')


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.debug = True
    app.run()