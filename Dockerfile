FROM ubuntu:20.04
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    apt-get install -y python-dev && \
    pip3 install -r /app/requirements.txt

COPY validate.py /app
COPY wsgi.py /app
CMD gunicorn --certfile=/certs/webhook.crt --keyfile=/certs/webhook.key --bind 0.0.0.0:443 wsgi:webhook