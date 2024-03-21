import requests
import json
from config import get_settings


# Step 0 - get the access token
def get_access_token():
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
    return access_token

# Step 1 - get PDF with the basic template
def test_basic_template(access_token, format="pdf"):
    data = {"source": "= Introduction\n#lorem(400)",
            "filename": "hello_basic_template",
            "format": format}
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}

    res = requests.post("http://127.0.0.1:8000/get_basic_template",
                headers = headers, 
                data = json.dumps(data))
    if res.status_code == 200:
        filename = res.headers['content-disposition'].split('=')[1]
        with open(f"pdfs/{filename}", "wb") as fp:
            fp.write(res.content)

# Step 2 - get PDF with the PRC template
def test_prc_template(access_token, format="pdf"):
    data = {"patientname": "Yubin Park",
            "pvalue1": "123456789A",
            "pvalue2": "9876B",
            "pvalue3": "March 1st, 2002",
            "pvalue4": "Male",
            "pvalue5": "0 in 2023",
            "pvalue6": "1 in 2023",
            "pvalue7": "March 1st, 2023",
            "pvalue8": "February 20th, 2024",
            "pvalue9": "Low Income", 
            "pvalue10": "NA",
            "rvalue1a": "HCC37",
            "rvalue1b": "Diabetes with Chronic Complications", 
            "rvalue1c": "We found that the patient's HbA1c value is above 6.5% and some other records of chronic complications", 
            "rvalue1d": "Open",
            "cvalue1a": "FLU",
            "cvalue1b": "We don't have a record of flue vaccine for the patient.",
            "cvalue1c": "Schedule a visit for flu vaccine",
            "cvalue1d": "Open",
            "filename": "hello_prc_template", 
            "format": format}
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}

    res = requests.post("http://127.0.0.1:8000/get_prc_template",
                headers = headers, 
                data = json.dumps(data))

    if res.status_code == 200:
        filename = res.headers['content-disposition'].split('=')[1]
        with open(f"pdfs/{filename}", "wb") as fp:
            fp.write(res.content)


if __name__ == "__main__":

    access_token = get_access_token()
    
    test_basic_template(access_token)
    test_prc_template(access_token)
    
    test_basic_template(access_token, "png")
    test_prc_template(access_token, "png")

    test_basic_template(access_token, "svg")
    test_prc_template(access_token, "svg")

    test_basic_template(access_token, "jpeg")
    test_prc_template(access_token, "jpeg")



