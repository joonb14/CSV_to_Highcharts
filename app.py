from flask import Flask, render_template
import pandas as pd
import numpy as np
import glob
import json
 
app = Flask(__name__)

@app.route('/')
@app.route('/graph')
def graph():
    files = glob.glob("*.csv")
    df=pd.read_csv(files[0], names=['Name','UUID','Major','Minor','formattedtime','time','temperature','humidity','rssi','data'])
    #Major over 10 is not the packet we want
    df=df[(df.Major < 10)]
    charttext = ['Temperature','Humidity']
    option =['temperature','humidity']
    ttext=['Temperature on iBeacons','Humidity on iBeacons']
    ytext=['Temperature','Humidity']
    chartInfo = []
    chart_type = 'line'
    chart_height = 500
    for i in range(2):
        chartID = charttext[i];
        chart = {"renderTo": chartID[i], "type": chart_type, "height": chart_height,}
        series = getSeries(df,option[i])
        title = {"text":ttext[i]}
        xAxis = {"type":"datetime"}
        yAxis = {"title":{"text":ytext[i]}}

        chartInfo.append([chartID, chart, series, title, xAxis, yAxis])

    return render_template('index.html', chartInfo=chartInfo)

def getSeries(df,option):
    #option is 'temperature' 'humidity'
    major_type = df.Major.unique()
    series = '['
    for i in range(len(major_type)):
        major = major_type[i]
        series += '{"name":"Major ' + str(major) + '","data":['
        for index, row in df.iterrows():
            if row['Major'] == major:
                series += '[' + str(row['time']) + ',' + str(int(row[option])) + '],'                   
        series = series[:-1]
        series += ']},'
    series = series[:-1] + ']'

    return series
 
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)
