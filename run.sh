#!/bin/sh
# export FLASK_APP=/app.py
# python -m flask run --host=0.0.0.0 --port=80
sed -i "s/##CLIENTID##/$CLIENTID/" /root/.netatmo.credentials
sed -i "s/##CLIENTSECRET##/$CLIENTSECRET/" /root/.netatmo.credentials
sed -i "s/##USERNAME##/$USERNAME/" /root/.netatmo.credentials
sed -i "s/##PASSWORD##/$PASSWORD/" /root/.netatmo.credentials

python /app.py
