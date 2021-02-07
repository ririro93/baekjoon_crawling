FROM python:3.8.7-alpine3.13

COPY requirements.txt /app/requirements.txt

RUN set -ex \
    && pip install --upgrade pip \  
    && pip install --no-cache-dir -r /app/requirements.txt 

# Working directory
WORKDIR /app

ADD . .

## for local dev
# EXPOSE 8000

# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "crawling_site.wsgi:application"]

## for deployment to heroku
# $PORT는 heroku가 알아서 지정해주는 애
CMD gunicorn crawling_site.wsgi:application --bind 0.0.0.0:$PORT