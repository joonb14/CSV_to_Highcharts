from flask import Flask, render_template
import pandas as pd
import numpy as np
import glob
import json
 
app = Flask(__name__)

@app.route('/about')
def aboutpage():

    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)


@app.route('/about/contact')
def contactPage():

    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)


@app.route('/')
@app.route('/graph')
def graph(chart_type = 'line', chart_height = 500):
    files = glob.glob("*-*-*_*-*-*.csv")
    df=pd.read_csv(files[0], names=['Name','UUID','Major','Minor','formattedtime','time','temperature','humidity','rssi','data'])
    #Major over 10 is not the packet we want
    df=df[(df.Major < 10)]
    charttext = ['Temperature','Humidity']
    option =['temperature','humidity']
    ttext=['Temperature on iBeacons','Humidity on iBeacons']
    ytext=['Temperature','Humidity']
    chartInfo = []
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
