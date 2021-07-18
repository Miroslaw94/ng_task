FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /ng_task
WORKDIR /ng_task
COPY ./ng_task /ng_task
