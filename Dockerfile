# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /home/mimi-pdf-service

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn main:app --reload --host 0.0.0.0
