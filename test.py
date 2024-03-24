import requests
import json
import csv
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

def _get_sample_pas_form(i=0, format="pdf"):
    """The sample data is generated with LLMs with the prompting script as follows:

I am writing a prior authorization letter for my patient. I have an authorization letter template, and  I need to fill in the blanks bracketed as follows:
---
The [procedure name] is clinically appropriate for my patient as [reasons for appropriateness]. In addition, your health plan's coverage policy states that the [procedure name] is considered medically necessary for patients with [risk factors].
---
An example letter for the S-ICD System (Subcutaneous Implantable Defibrillator) implantation is as follows:
---
The [S-ICD System] is clinically appropriate for my patient as [the patient does not have symptomatic bradycardia, incessant ventricular tachycardia, or spontaneous, frequently recurring ventricular tachycardia that is reliably terminated with anti-tachycardia pacing]. In addition, your health plan's coverage policy states that the [S-ICD System] is considered medically necessary for patients with [Brugada syndrome].
---
For a given [procedure name], I want the answers in the following JSON format:
{
  "reason for appropriateness": "",
  "risk factors": ""
}

Let's start with the procedure name, "Bariatric Surgery." Let's think step by step in order to produce the answer. Go!
    """
    pas_form = {"filename": f"priorauth_surgery_sample{i}",
                "format": format,
                "insurancecompanyname": "UnitedHealthcare",
                "patientname": "Yubin Park",
                "policyholdername": "Yubin Park",
                "patientid": "123456789A",
                "claimid": "CLAIM1234567890",
                "procedurename": "Bariatric Surgery",
                "surgerydate": "05/21/2024",
                "reasonsforappropriateness": "my patient has a BMI of 40 kg/m2 and has unsuccessfully attempted weight loss through diet, exercise, and pharmacotherapy. These conditions significantly increase the risk of morbidity and mortality, and bariatric surgery has been proven to effectively reduce weight, improve or resolve comorbidities, and enhance quality of life",
                "riskfactors": "a BMI of 40 kg/m2",
                "faxnumber": "123-456-7890",
                "phonenumber": "987-654-3210",
                "doctorname": "Yubin Park, MD",
                "practicename": "Park Practice"
                }
    return pas_form

# Step 6 - Prior Authorization Letter
def test_pas_template(access_token, address, format="pdf"):
    pas_form = _get_sample_pas_form(0, format) 
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_pas_template",
                headers = headers, 
                data = json.dumps(pas_form))
    if res.status_code == 200:
        filename = res.headers['content-disposition'].split('=')[1]
        with open(f"test_outputs/{filename}", "wb") as fp:
            fp.write(res.content)

def _get_sample_pam_form(i=0, format="pdf"):
    """The sample data is generated with LLMs with the prompting script as follows:

I am writing a prior authorization letter for my patient. I have an authorization letter template, and  I need to fill in the blanks bracketed as follows:
---
I have prescribed [product name] because this patient has been diagnosed with [diagnosis]. [product name] is indicated for [indications]. [reasons for appropriateness]
---
An example letter for Zinplava is as follows:
---
I have prescribed [Zinplava] because this patient has been diagnosed with [severe CDI]. [Zinplava] is indicated for [reducing the recurrence of CDI]. [The decision is based on the facts that the patient had multiple CDIs in the past six months and is older than 65 years, and given the patient's immunocompromised situation.]
---
For a given [procedure name], I want the answers in the following JSON format:
{
  "diagnosis": "",
  "indications": "",
  "reason for appropriateness": ""
}
Let's start with the product name, "Humira." Let's think step by step in order to produce the answer. Go!

    """
    pam_form = {"filename": f"priorauth_medication_sample{i}",
                "format": format,
                "insurancecompanyname": "UnitedHealthcare",
                "patientname": "Yubin Park",
                "policyholdername": "Yubin Park",
                "patientid": "123456789A",
                "claimid": "CLAIM1234567890",
                "productname": "Humira",
                "diagnosis": "severe rheumatoid arthritis",
                "indications": "reducing signs and symptoms, inducing major clinical response, inhibiting the progression of structural damage, and improving physical function in adult patients",
                "reasonsforappropriateness": "The decision is based on the patient's inadequate response to one or more DMARDs, the need to slow disease progression and structural damage, and improve physical function and quality of life. Considering patient-specific factors such as age, disease severity, comorbidities, and tolerability to previous treatments also supports this decision.",
                "faxnumber": "123-456-7890",
                "phonenumber": "987-654-3210",
                "doctorname": "Yubin Park, MD",
                "practicename": "Park Practice"
                }
    return pam_form

# Step 7 - Prior Authorization Letter - Meds
def test_pam_template(access_token, address, format="pdf"):
    pam_form = _get_sample_pam_form(0, format) 
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_pam_template",
                headers = headers, 
                data = json.dumps(pam_form))
    if res.status_code == 200:
        filename = res.headers['content-disposition'].split('=')[1]
        with open(f"test_outputs/{filename}", "wb") as fp:
            fp.write(res.content)

# Step 8
def test_bulk_pas_template(access_token, address, format="pdf"):
    pas_forms = [_get_sample_pas_form(i, format) for i in range(0, 3)]
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_pas_template_in_bulk",
                headers = headers, 
                data = json.dumps(pas_forms))
    if res.status_code == 200:
        for output_item in res.json():
            filename = output_item["filename"]
            with open(f"test_outputs/{filename}", "wb") as fp:
                fp.write(base64.b64decode(output_item["bytestring"]))

# Step 9
def test_bulk_pam_template(access_token, address, format="pdf"):
    pam_forms = [_get_sample_pam_form(i, format) for i in range(0, 3)]
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_pam_template_in_bulk",
                headers = headers, 
                data = json.dumps(pam_forms))
    if res.status_code == 200:
        for output_item in res.json():
            filename = output_item["filename"]
            with open(f"test_outputs/{filename}", "wb") as fp:
                fp.write(base64.b64decode(output_item["bytestring"]))

# Step 10
def test_bulk_speed(access_token, address, bulk_cnt, format="pdf"):

    start = time.time()
    prc_forms = [_get_sample_prc_form(i, format) for i in range(0, bulk_cnt)]
    headers = {"content-type": "application/json",
               "Authorization": ("Bearer " + access_token)}
    res = requests.post(f"{address}/use_prc_template_in_bulk",
                headers = headers, 
                data = json.dumps(prc_forms))
    end = time.time()

    time_tot = end - start
    time_avg = time_tot / bulk_cnt

    return bulk_cnt, time_tot, time_avg

 
if __name__ == "__main__":

    access_token = get_access_token()
    address = "https://pdfservices.mimilabs.org" 
    #address = "http://127.0.0.1:8000" 
    
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

    test_pas_template(access_token, address)
    test_pas_template(access_token, address, "png")
    test_bulk_pas_template(access_token, address)

    test_pam_template(access_token, address)
    test_pam_template(access_token, address, "png")
    test_bulk_pam_template(access_token, address)
    
    data = [["cnt", "time_tot", "time_avg"]]
    for i in range(5): # 5 batches of experiments
        for bulk_cnt in [1, 5, 10, 20, 30, 40, 50]:
            d = test_bulk_speed(access_token, address, bulk_cnt)
            print(f"[SpeedTest] {str(d)}")
            data.append(d)
    with open("test_outputs/speed_test.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerows(data)

