import datetime

from flask import Flask, render_template, json, request
from flask_bootstrap import Bootstrap
from google.cloud import datastore

app = Flask(__name__)
bootstrap = Bootstrap(app)

datastore_client = datastore.Client()

def getdata(time):
    date = datetime.datetime.strptime(time, '%Y-%m-%d')
    query = datastore_client.query(kind='rainfall_data')
    query.add_filter('datetime', '=', date)

    return query.fetch()

def loopdata(time):
    database = getdata(time)
    dataListAll = []
    for x in database:
        datetime = x['datetime']
        lat = x['lat']
        lng = x['lng']
        rainfall = x['rainfall']
        station_id = x['station_id']
        dataList = [datetime.strftime('%Y-%m-%d'), lat, lng, rainfall, station_id]
        dataListAll.append(dataList)
    return dataListAll

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/index/',methods=['GET','POST'])
def get_date():
    time = request.form.get('time')
    dataListAll = loopdata(time)
    return render_template('index.html', dataListAll=json.dumps(dataListAll),time =time)

if __name__ == '__main__':
    app.run()
