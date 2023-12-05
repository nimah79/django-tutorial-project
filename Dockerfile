FROM python:3.12-slim-bullseye

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install gcc default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
