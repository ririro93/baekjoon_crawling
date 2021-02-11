FROM python:3.8.7-alpine3.13

# Working directory
WORKDIR /usr/src/app

# set env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
COPY requirements.txt /app/requirements.txt
RUN set -ex \
    && pip install --upgrade pip \  
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apk add --no-cache tzdata

# copy entrypoint.sh -> 밑에서 모든 파일 다 복사하지만 이렇게 안하면 밑에꺼가 실행이안됨ㅎㅎ..
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
# # for local dev
# EXPOSE 8000

# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "crawling_site.wsgi:application"]

# for deployment to heroku
# $PORT는 heroku가 알아서 지정해주는 애
CMD gunicorn crawling_site.wsgi:application --bind 0.0.0.0:$PORT