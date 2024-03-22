#!/bin/bash

aws ecr create-repository --repository-name mimi-pdf-services --region us-east-2

docker tag mimi-pdf-services 533267369554.dkr.ecr.us-east-2.amazonaws.com/mimi-pdf-services	

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 533267369554.dkr.ecr.us-east-2.amazonaws.com

docker push 533267369554.dkr.ecr.us-east-2.amazonaws.com/mimi-pdf-services:latest


