#FROM python:3.9-alpine3.16

#RUN adduser --disabled-password service-user
#
#COPY requirements.txt /temp/requirements.txt
#RUN /usr/local/bin/python -m pip install --upgrade pip
#RUN pip install -r /temp/requirements.txt
#
#COPY service /service
#WORKDIR /service
#EXPOSE 8000
#
#RUN apk add postgresql-client build-base postgresql-dev libpq-dev
#
#USER service-user

FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY service /service
WORKDIR /service
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev libpq-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user