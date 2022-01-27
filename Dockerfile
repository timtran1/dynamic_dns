FROM python:3.9-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

COPY crontab /tmp/crontab
RUN cat /tmp/crontab > /etc/crontabs/root

CMD ["crond", "-f", "-l", "2"]