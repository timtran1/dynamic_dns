FROM python:3.12-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

COPY config.json.sample /app/config.json

COPY crontab /tmp/crontab
RUN cat /tmp/crontab > /etc/crontabs/root

CMD ["crond", "-f", "-l", "2"]