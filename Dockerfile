FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk --update add vim gcc libc-dev

COPY ./requirements.txt /var/www/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r /var/www/requirements.txt
