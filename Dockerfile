# syntax=docker/dockerfile:1

# Use the Rust:Alpine image as the base
FROM ghcr.io/typst/typst:latest

# Install Python and pip
RUN apk add --update --no-cache python3 py3-pip

WORKDIR /home/mimi-pdf-service

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
