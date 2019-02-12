FROM python:3.6-jessie

ENV TZ=Europe/Istanbul

COPY . /app
WORKDIR /app
RUN pip install -r ./requirements.txt
RUN make test

WORKDIR /app/src
ENV PYTHONPATH=/app