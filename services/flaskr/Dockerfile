FROM osgeo/gdal:alpine-small-latest
WORKDIR /usr/src/app
# dont write .pyc to disc
ENV PYTHONDONTWRITEBYTECODE 1
# prevents stdout and stderr buffering
ENV PYTHONUNBUFFERED 1

run apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev g++

RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt

RUN pip3 install GDAL

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]