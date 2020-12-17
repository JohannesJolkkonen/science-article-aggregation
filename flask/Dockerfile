FROM python:3.7.2-stretch

WORKDIR /app 

COPY requirements.txt .

RUN pip install -r requirements.txt 

ADD . /app

CMD ["uwsgi", "app.ini"]

## Make a dummy app which returns working directory in the browser-view for debugging.