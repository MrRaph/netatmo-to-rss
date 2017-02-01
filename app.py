import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
import time
import os
import requests
import json
import logging
import lnetatmo
import pytz
import PyRSS2Gen
# from urlparse import urljoin
from flask import Flask, request
from werkzeug.contrib.atom import AtomFeed

app = Flask(__name__)

# def make_external(url):
#     return urljoin(request.url_root, url)

# global feed

def getNetatmoData(feed):
    # print(devList.lastData()['Balcon']['Temperature'])
    # print(
    #     datetime.fromtimestamp(
    #         int(devList.lastData()['Balcon']['When'])
    #     ).strftime('%d-%m-%Y %H:%M:%S')
    # )
    authorization = lnetatmo.ClientAuth()
    devList = lnetatmo.WeatherStationData(authorization)

    when = datetime.fromtimestamp(
            int(devList.lastData()['Balcon']['When'])
        )

    string = str(devList.lastData()['Balcon']['Temperature']) + " °C at " + str(datetime.fromtimestamp(
            int(devList.lastData()['Balcon']['When'])
        ).strftime('%d-%m-%Y %H:%M:%S'))

    feed.add(string, string, content_type='html',
             author="", url="", id=devList.lastData()['Balcon']['When'],
             updated=when, published=when)

@app.route('/')
def generateRSS():
    feed = AtomFeed("Temperature", feed_url=request.url,
        url=request.host_url,
        subtitle="AldaNet")
    getNetatmoData(feed)
    return feed.get_response()

if __name__ == '__main__':

    # log = logging.getLogger('apscheduler.executors.default')
    # log.setLevel(logging.INFO)  # DEBUG
    #
    # fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    # h = logging.StreamHandler()
    # h.setFormatter(fmt)
    # log.addHandler(h)
    #
    # timezone = pytz.timezone('Europe/Paris')
    # scheduler = BackgroundScheduler(timezone=timezone)
    #
    # authorization = lnetatmo.ClientAuth()
    # devList = lnetatmo.WeatherStationData(authorization)
    #
    # job = scheduler.add_job(getNetatmoData, 'interval', minutes=1)
    # scheduler.start()

    app.run(debug=True, host='0.0.0.0', port=80)
    # try:
    #     while True:
    #         time.sleep(2)
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
