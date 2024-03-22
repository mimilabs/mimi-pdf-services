
## Building the image
```
docker build -t mimi-pdf-services .
```

## Running the image
```
docker run -it -p 8000:8000 mimi-pdf-services
```

## Running the FastAPI server inside the image
```
uvicorn main:app --reload --host 0.0.0.0
```

## Running the image on AWS

```
aws ecr create-repository --repository-name mimi-pdf-services --region <region>
```

```
docker tag mimi-pdf-services <aws_account_id>.dkr.ecr.<region>.amazonaws.com/mimi-pdf-services
```

```
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.region.amazonaws.com
```

```
docker push aws_account_id.dkr.ecr.region.amazonaws.com/mimi-pdf-services
```



aws ecr create-repository --repository-name mimi-pdf-services --region us-east-2

docker tag mimi-pdf-services 533267369554.dkr.ecr.us-east-2.amazonaws.com/mimi-pdf-services	

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 533267369554.dkr.ecr.us-east-2.amazonaws.com

docker push 533267369554.dkr.ecr.us-east-2.amazonaws.com/mimi-pdf-services:latest



## Auth0 Authentication

- https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
- https://github.com/auth0-blog/auth0-python-fastapi-sample/tree/main

