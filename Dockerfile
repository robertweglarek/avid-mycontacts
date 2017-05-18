FROM python:3.6-alpine

# Install libs
RUN apk add --no-cache --update build-base \
    postgresql-dev \
    bash \
    && rm /var/cache/apk/*

# Prepare the app
RUN mkdir /app
WORKDIR /app
ADD . /app

# Install libs
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
