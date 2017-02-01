from datetime import datetime
import time
import os
import requests
import lnetatmo
import pytz
import PyRSS2Gen
import os.path
from flask import Flask, request, Response

app = Flask(__name__)
app.config.from_object(__name__)

global items, rss


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))
def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

def getNetatmoData():
    authorization = lnetatmo.ClientAuth()
    devList = lnetatmo.WeatherStationData(authorization)

    when = datetime.fromtimestamp(
            int(devList.lastData()['Balcon']['When'])
        )

    string = str(devList.lastData()['Balcon']['Temperature']) + " °C at " + str(datetime.fromtimestamp(
            int(devList.lastData()['Balcon']['When'])
        ).strftime('%d-%m-%Y %H:%M:%S'))

    rss.items = [PyRSS2Gen.RSSItem(
        title = string,
        link = "",
        description = string,
        pubDate = when
    )]

    rss.lastBuildDate = when
    rss.write_xml(open("/pyrss2gen.xml", "w"))

@app.route('/', methods=['GET'])
def serverRSS():
    getNetatmoData()

    content = get_file('/pyrss2gen.xml')
    return Response(content, mimetype="text/xml")

if __name__ == '__main__':

    items = []

    rss = PyRSS2Gen.RSS2(
        title = "Temperature",
        link = "",
        description = "Temperature",
        lastBuildDate = datetime.now(),
        items = items
    )

    app.run(debug=True, host='0.0.0.0', port=80)
