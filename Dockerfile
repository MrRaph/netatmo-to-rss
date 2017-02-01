FROM python:alpine

ADD ./app.py /app.py
ADD ./run.sh /run.sh
ADD ./requirements.txt /requirements.txt
ADD ./.netatmo.credentials /root/.netatmo.credentials

RUN pip install -r /requirements.txt && \
    chmod +x /run.sh

EXPOSE 80
CMD ["/run.sh"]
