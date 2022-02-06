FROM python:3.11.0a5-alpine3.15

RUN apk --update add gcc libc-dev

WORKDIR /app

COPY . ./

RUN pip install -r /app/requirements.txt

ENV PORT 80

CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
