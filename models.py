from pydantic import BaseModel
from typing import Literal, List

LOGO_LIST = Literal["\"mimilabs.png\"", 
                   "\"auth0.png\"", 
                   "\"fastapi.png\"", 
                   "\"auth0.png\""]

class BasicForm(BaseModel):
    content: str
    format: Literal["pdf", "png", "svg"]
    filename: str = "raw_tmp"
    headerlogo: LOGO_LIST = "\"mimilabs.png\""
    footertext: str = "mimilabs.ai - Beautiful Small Projects, One by One"

class PrcForm(BaseModel):
    format: Literal["pdf", "png", "svg"]
    filename: str = "prc_tmp"
    headerlogo: LOGO_LIST = "\"mimilabs.png\""
    footertext: str = "mimilabs.ai - Beautiful Small Projects, One by One"
    patientname: str = "\[Patient Name\]"
    formname: str = "Annual Wellness Visit Form"
    psection: str = "Profile"
    pdescription: str = "The profile information is based on CMS's Claim and Claim Line Feed (CCLF) data."
    rsection: str = "Risk Factor Snapshot"
    rdescription: str = "The risk factor snapshot is based on previous claims data, Admission-Discharge-Transfer (ADT) data feed, and Health Information Exchange (HIE) data. Please check if these factors exist, and if so, please document those in the EHR."
    csection: str = "Care Gap Snapshot"
    cdescription: str = "The care gap snapshot is based on previous claims data - some recent data may not be reflected. Please check if the patient has any open care gaps."
    pname1: str = "Patient ID"
    pvalue1: str = ""
    pname2: str = "MRN"
    pvalue2: str = ""
    pname3: str = "Date of Birth"
    pvalue3: str = ""
    pname4: str = "Gender"
    pvalue4: str = ""
    pname5: str = "Hosp. Count"
    pvalue5: str = ""
    pname6: str = "ED Count"
    pvalue6: str = ""
    pname7: str = "Last AWV Date"
    pvalue7: str = ""
    pname8: str = "Last Visit Date"
    pvalue8: str = ""
    pname9: str = "SDoH"
    pvalue9: str = ""
    pname10: str = "Misc."
    pvalue10: str = ""
    rname1a: str = "HCC"
    rname1b: str = "Description"
    rname1c: str = "Evidence"
    rname1d: str = "Status"
    rvalue1a: str = ""
    rvalue1b: str = ""
    rvalue1c: str = ""
    rvalue1d: str = ""
    rvalue2a: str = ""
    rvalue2b: str = ""
    rvalue2c: str = ""
    rvalue2d: str = ""
    rvalue3a: str = ""
    rvalue3b: str = ""
    rvalue3c: str = ""
    rvalue3d: str = ""
    rvalue4a: str = ""
    rvalue4b: str = ""
    rvalue4c: str = ""
    rvalue4d: str = ""
    rvalue5a: str = ""
    rvalue5b: str = ""
    rvalue5c: str = ""
    rvalue5d: str = ""
    rvalue6a: str = ""
    rvalue6b: str = ""
    rvalue6c: str = ""
    rvalue6d: str = ""
    rvalue7a: str = ""
    rvalue7b: str = ""
    rvalue7c: str = ""
    rvalue7d: str = ""
    rvalue8a: str = ""
    rvalue8b: str = ""
    rvalue8c: str = ""
    rvalue8d: str = ""
    rvalue9a: str = ""
    rvalue9b: str = ""
    rvalue9c: str = ""
    rvalue9d: str = ""
    rvalue10a: str = ""
    rvalue10b: str = ""
    rvalue10c: str = ""
    rvalue10d: str = ""
    cname1a: str = "Name"
    cname1b: str = "Description"
    cname1c: str = "To Do"
    cname1d: str = "Status"
    cvalue1a: str = ""
    cvalue1b: str = ""
    cvalue1c: str = ""
    cvalue1d: str = ""
    cvalue2a: str = ""
    cvalue2b: str = ""
    cvalue2c: str = ""
    cvalue2d: str = ""
    cvalue3a: str = ""
    cvalue3b: str = ""
    cvalue3c: str = ""
    cvalue3d: str = ""
    cvalue4a: str = ""
    cvalue4b: str = ""
    cvalue4c: str = ""
    cvalue4d: str = ""
    cvalue5a: str = ""
    cvalue5b: str = ""
    cvalue5c: str = ""
    cvalue5d: str = ""

BasicForms = List[BasicForm]
PrcForms = List[PrcForm]

class BulkItem(BaseModel):
    bytestring: str
    processing_time: float
    filename: str

BulkOutput = List[BulkItem]


