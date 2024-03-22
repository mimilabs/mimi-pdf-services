import requests
import json
from config import get_settings
import time
import hashlib
import base64

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

# Step 1 - get PDF with a blank template
def test_blank_template(access_token, 
                        address, 
                        format="pdf"):
    
    filename = "test_blank"
    data = {"content": "= Introduction\n#lorem(400)",
            "filename": filename,
            "format": format}
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_blank_template",
                headers = headers, 
                data = json.dumps(data))
    if res.status_code == 200:
        filename = res.headers['content-disposition'].split('=')[1]
        with open(f"test_outputs/{filename}", "wb") as fp:
            fp.write(res.content)

# Step 2 - get PDF with the basic template
def test_basic_template(access_token, 
                        address, 
                        headerlogo = "\"mimilabs.png\"",
                        footertext = "Custom Header",
                        format="pdf"):
    
    h = hashlib.new('sha256') 
    h.update((headerlogo + footertext).encode())
    filename = "test_basic_" + h.hexdigest()[:8]
    data = {"content": "= Introduction\n#lorem(400)",
            "filename": filename,
            "headerlogo": headerlogo,
            "footertext": footertext,
            "format": format}
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_basic_template",
                headers = headers, 
                data = json.dumps(data))
    if res.status_code == 200:
        filename = res.headers['content-disposition'].split('=')[1]
        with open(f"test_outputs/{filename}", "wb") as fp:
            fp.write(res.content)

def _get_sample_prc_form(index=0, format="pdf"):
    filename = f"test_prc_{index}"
    sample_data = {"patientname": "Yubin Park",
            "pvalue1": f"123456789A{index}",
            "pvalue2": f"9876B{index}",
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
            "rvalue1c": ("We found that the patient's HbA1c value "
                        "is above 6.5% and some other records of "
                        "chronic complications"), 
            "rvalue1d": "Open",
            "cvalue1a": "FLU",
            "cvalue1b": ("We don't have a record of flue vaccine "
                        "for the patient."),
            "cvalue1c": "Schedule a visit for flu vaccine",
            "cvalue1d": "Open",
            "filename": filename, 
            "format": format}
    return sample_data


# Step 3 - get PDF with the PRC template
def test_prc_template(access_token, address, format="pdf"):
    
    prc_form = _get_sample_prc_form(0, format)
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_prc_template",
                headers = headers, 
                data = json.dumps(prc_form))
    if res.status_code == 200:
        filename = res.headers['content-disposition'].split('=')[1]
        with open(f"test_outputs/{filename}", "wb") as fp:
            fp.write(res.content)

# Step 4 - get bulk PDFs with the PRC template
def test_bulk_prc_template(access_token, address, format="pdf"):
    
    prc_forms = [_get_sample_prc_form(i, format) for i in range(0, 10)]
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_prc_template_in_bulk",
                headers = headers, 
                data = json.dumps(prc_forms))
    if res.status_code == 200:
        for output_item in res.json():
            filename = output_item["filename"]
            with open(f"test_outputs/{filename}", "wb") as fp:
                fp.write(base64.b64decode(output_item["bytestring"]))

# Step 5 - get bulk PDFs with the Basic template
def test_bulk_basic_template(access_token, address, format="pdf"):
    
    basic_forms = [{"content": f"= Introduction\n#lorem({i*10})",
                "filename": f"basic_template_{i}",
                "headerlogo": "\"mimilabs.png\"",
                "footertext": "mimilabs is love",
                "format": format}
                    for i in range(0, 10)]
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_basic_template_in_bulk",
                headers = headers, 
                data = json.dumps(basic_forms))
    if res.status_code == 200:
        for output_item in res.json():
            filename = output_item["filename"]
            with open(f"test_outputs/{filename}", "wb") as fp:
                fp.write(base64.b64decode(output_item["bytestring"]))

if __name__ == "__main__":

    access_token = get_access_token()
    #address = "3.15.203.240" 
    address = "http://127.0.0.1:8000" 
  
    
    test_blank_template(access_token, address)
    test_blank_template(access_token, address, "png")
    
    test_basic_template(access_token, address)
    test_basic_template(access_token, address, 
                        "\"auth0.png\"", "auth0 - security")
    test_basic_template(access_token, address,
                        "\"fastapi.png\"", "fastapi test")
    test_basic_template(access_token, address, format="png")

    test_prc_template(access_token, address, "pdf")
    test_prc_template(access_token, address, "svg")
    test_prc_template(access_token, address, "png")
    
    test_bulk_prc_template(access_token, address)

    test_bulk_basic_template(access_token, address)

