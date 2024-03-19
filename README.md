
## Building the image
```
docker build -t test-app .
```

## Running the image
```
docker run -it -p 8000:8000 test-app
```

## Running the FastAPI server inside the image
```
uvicorn main:app --reload --host 0.0.0.0
```


## Auth0 Authentication

- https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
- https://github.com/auth0-blog/auth0-python-fastapi-sample/tree/main

