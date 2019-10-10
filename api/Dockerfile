FROM python:3.6-slim

RUN pip install --upgrade pip
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt

EXPOSE 5000
