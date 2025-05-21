FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y python3-opencv && \
    pip install -r requirements.txt