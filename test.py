import requests
import json
from config import get_settings


# Step 0 - get the access token


env_settings = get_settings()
data = {"client_id": env_settings.auth0_client_id,
        "client_secret": env_settings.auth0_client_secret,
        "audience": env_settings.auth0_api_audience,
        "grant_type": "client_credentials"}

headers = {"content-type": "application/json" }

res = requests.post(f"https://{env_settings.auth0_domain}/oauth/token", 
                    headers = headers,
                    data = json.dumps(data))
access_token = res.json()["access_token"]


# Step 1 - get PDF with the blank template

data = {"source": """= Introduction
            In this report, we will explore the various factors 
            that influence _fluid dynamics_ in glaciers and how 
            they contribute to the formation and behaviour of 
            these natural structures.""", 
        "filename": "hello_blank_template"}
headers = {"content-type": "application/json",
           "Authorization": ("Bearer " + access_token)}

res = requests.post("http://127.0.0.1:8000/get_pdf_basic_template",
            headers = headers, 
            data = json.dumps(data))
print(res)
#print(res.headers['mimi-processing-time'])

filename = res.headers['content-disposition'].split('=')[1]
with open(f"pdfs/{filename}", "wb") as fp:
    fp.write(res.content)
