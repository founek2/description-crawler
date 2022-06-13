FROM python:3.9-buster

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./src ./src

ENV FLASK_APP=/app/src/server.py

CMD flask run -h 0.0.0.0