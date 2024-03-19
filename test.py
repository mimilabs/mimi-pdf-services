import requests
import json

# Step 0 - get the access token

data = {"client_id": "WQ1YObTwdv2ypaUAysMVTrydOKjIsPyr",
        "client_secret": "MS76iF04Qa1d_oVbMRAZxt-w-PYY1msXCBG6OMM0xdUIR3uDy-mZZFeD1R9mq96x",
        "audience": "https://pdfservice.mimilabs.ai",
        "grant_type": "client_credentials"}

headers = {"content-type": "application/json" }

res = requests.post("https://dev-2f3aykbpxd0x4dbi.us.auth0.com/oauth/token", 
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

res = requests.post("http://127.0.0.1:8000/get_pdf_blank_template",
                headers = headers, 
                data = json.dumps(data))

filename = res.headers['content-disposition'].split('=')[1]
with open(f"pdfs/{filename}", "wb") as fp:
    fp.write(res.content)
