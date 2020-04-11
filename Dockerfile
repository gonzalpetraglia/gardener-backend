FROM python:3.6-alpine

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY ./src /app3

ENV FLASK_APP=/app/main.py

EXPOSE  5000
ENTRYPOINT flask run --host=0.0.0.0
