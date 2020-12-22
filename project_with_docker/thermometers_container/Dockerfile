FROM python:3.7.2-alpine3.8
RUN apk update && apk upgrade && apk add bash


RUN pip install --upgrade pip
RUN pip install paho-mqtt
WORKDIR /thermometers_container/
