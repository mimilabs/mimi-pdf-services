from fastapi import FastAPI, Response, Security
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import HTTPException
import os
import time
from string import Template
import base64
import typst
from utils import VerifyToken
from pathlib import Path
import tempfile
from models import (BasicForm, BasicForms,
                    PrcForm, PrcForms,
                    PasForm, PasForms,
                    PamForm, PamForms,
                    BulkOutput)

# create an API server
app = FastAPI(
    title="mimi-pdf-services",
    summary="mimi-pdf-services can generate a lot of PDFs very fast",
    description="""mimi-pdf-services is a light-weight and fast PDF generation
service. To use this service, you can ask info@mimilabs.ai to get the Auth0-based 
API key (easy) or you can download the source code and use the source code 
directly (hard, but more customaizable).""",
    version="0.0.1",
    contact={
            "name": "mimilabs.ai",
            "url": "https://mimilabs.ai",
            "email": "info@mimilabs.ai"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    docs_url=None,
    redoc_url=None
)
auth = VerifyToken()  # use Auth0 API-Key

# work directory
# - this is the folder where raw Typst sources and image files are stored
WORK_DIR = "./workdir"

# load all templates
basic_template = Template(open('templates/basic_template.typ').read())
prc_template = Template(open('templates/prc_template.typ').read())
pas_template = Template(open('templates/pas_template.typ').read())
pam_template = Template(open('templates/pam_template.typ').read())

# Change favicon for the docs and redoc


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(openapi_url="/openapi.json",
                               title=app.title + " - Swagger UI",
                               swagger_favicon_url="https://www.mimilabs.ai/favicon.ico")


@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(openapi_url="/openapi.json",
                          title=app.title + " - Redoc",
                          redoc_favicon_url="https://www.mimilabs.ai/favicon.ico")


def _run_typst(source: str, format: str):
    """
    This function compiles the Typst source into a PDF (or PNG, SVG).
    """
    start = time.time()
    fpath = WORK_DIR

    # create a temp file to run Typst
    with tempfile.NamedTemporaryFile(dir=WORK_DIR,
                                     mode='w',
                                     delete=False) as fp:
        fp.write(source)
        fpath = fp.name

    # compile the Typst source
    try:
        output = typst.compile(fpath, format=format)
    except RuntimeError as e:
        raise HTTPException(status_code=500,
                            detail=str(e),
                            headers={"X-Error": "Typst compile error"})

    os.remove(fpath)  # remove the temp file

    end = time.time()  # measure the compile + misc. time
    processing_time = end - start

    return output, processing_time


def _make_single(source: str, filename: str, format: str):
    """
    Wraps a single document output into a Response object.
    """
    output, processing_time = _run_typst(source, format)
    return Response(content=output,
                    media_type=f"application/{format}",
                    headers={"Content-Disposition": ('attachment; ' +
                                                     f'filename={filename}.{format}'),
                             "MIMI-Processing-Time": str(processing_time)})


def _make_bulk(forms, template):
    """
    Wraps multiple documents into an array of List(BulkItem), 
    i.e., BulkOutput. 
    NOTE: If the number of forms is more than 50, it raises an error.
    """
    output_array = []
    p_time_tot = 0
    if len(forms) > 50:
        raise HTTPException(status_code=500,
                            detail=str(e),
                            headers={"X-Error": ("Too many documents."
                                                 "Should be less than 50.")})

    for form in forms:
        output, p_time = _run_typst(
            template.substitute(**form.__dict__),
            form.format)
        p_time_tot += p_time
        filename = Path(form.filename).stem + "." + form.format
        output_array.append({"bytestring": base64.b64encode(output),
                             "processing_time": p_time,
                             "filename": filename})
    return output_array, p_time_tot

@app.get('/')
async def read_main():
    return {"msg": """Please use the API endpoints to generate PDFs.
For more information, please visit the documentation page at
https://pdfservices.mimilabs.org/docs."""}

@app.post('/use_blank_template')
async def use_blank_template(basic_form: BasicForm,
                             auth_result: str = Security(auth.verify)) -> Response:
    """
    Create a document with no header and no footer, 
    i.e., blank template.
    The headerlog and footertext parameters are ignored.
    """
    return _make_single(basic_form.content,
                        Path(basic_form.filename).stem,
                        basic_form.format)


@app.post('/use_basic_template')
async def use_basic_template(basic_form: BasicForm,
                             auth_result: str = Security(auth.verify)) -> Response:
    """
    Create a document with basic header and footer. 
    The headerlogo and footertext parameters can be 
    customizable. However, the headerlogo file should exist in 
    the work directory. 
    """
    return _make_single(basic_template.substitute(**basic_form.__dict__),
                        Path(basic_form.filename).stem,
                        basic_form.format)


@app.post('/use_prc_template')
async def use_prc_template(prc_form: PrcForm,
                           auth_result: str = Security(auth.verify)) -> Response:
    """
    Create a PRC-template document, where PRC stands 
    for the Profile, Risk, and Quality sections. 
    However, one can change the PRC sections to any other names.
    For example, if you set `psection` as "Section A," 
    the first section name will show as "Section A," 
    not "Profile." The form is highly customizable.
    """
    return _make_single(prc_template.substitute(**prc_form.__dict__),
                        Path(prc_form.filename).stem,
                        prc_form.format)


@app.post('/use_pas_template')
async def use_pas_template(pas_form: PasForm,
                           auth_result: str = Security(auth.verify)) -> Response:
    """
    Create a PAS-template document, where PAS stands 
    for Prior Authorization for Surgery. You can generate 
    the contents either manually or with help with LLMs.
    """
    return _make_single(pas_template.substitute(**pas_form.__dict__),
                        Path(pas_form.filename).stem,
                        pas_form.format)


@app.post('/use_pam_template')
async def use_pam_template(pam_form: PamForm,
                           auth_result: str = Security(auth.verify)) -> Response:
    """
    Create a PAM-template document, where PAM stands 
    for Prior Authorization for Meds. You can generate 
    the contents either manually or with help with LLMs.
    """
    return _make_single(pam_template.substitute(**pam_form.__dict__),
                        Path(pam_form.filename).stem,
                        pam_form.format)


@app.post('/use_blank_template_in_bulk')
async def use_blank_template_in_bulk(basic_forms: BasicForms,
                                     response: Response,
                                     auth_result: str = Security(auth.verify)) -> BulkOutput:
    """
    Create a list of blank-template documents - 
    a bulk operation. Max 50. This endpoint 
    will return a list of PDF/PNG/SVG bytestrings. 
    You need to parse the output 
    appropriately to get the list of the output files.
    """
    output_array, p_time_tot = _make_bulk(basic_forms, basic_template)
    response.headers["MIMI-Processing-Time"] = str(p_time_tot)
    return output_array


@app.post('/use_basic_template_in_bulk')
async def use_basic_template_in_bulk(basic_forms: BasicForms,
                                     response: Response,
                                     auth_result: str = Security(auth.verify)) -> BulkOutput:
    """
    Create a list of basic-template documents - 
    a bulk operation. Max 50. This endpoint 
    will return a list of PDF/PNG/SVG bytestrings. 
    You need to parse the output 
    appropriately to get the list of the output files.
    """
    output_array, p_time_tot = _make_bulk(basic_forms, basic_template)
    response.headers["MIMI-Processing-Time"] = str(p_time_tot)
    return output_array


@app.post('/use_prc_template_in_bulk')
async def use_prc_template_in_bulk(prc_forms: PrcForms,
                                   response: Response,
                                   auth_result: str = Security(auth.verify)) -> BulkOutput:
    """
    Create a list of PRC-template documents - 
    a bulk operation. Max 50. This endpoint 
    will return a list of PDF/PNG/SVG bytestrings. 
    You need to parse the output 
    appropriately to get the list of the output files.
    """
    output_array, p_time_tot = _make_bulk(prc_forms, prc_template)
    response.headers["MIMI-Processing-Time"] = str(p_time_tot)
    return output_array


@app.post('/use_pas_template_in_bulk')
async def use_pas_template_in_bulk(pas_forms: PasForms,
                                   response: Response,
                                   auth_result: str = Security(auth.verify)) -> BulkOutput:
    """
    Create a list of PAS-template documents - 
    a bulk operation. Max 50. This endpoint 
    will return a list of PDF/PNG/SVG bytestrings. 
    You need to parse the output 
    appropriately to get the list of the output files.
    """
    output_array, p_time_tot = _make_bulk(pas_forms, pas_template)
    response.headers["MIMI-Processing-Time"] = str(p_time_tot)
    return output_array


@app.post('/use_pam_template_in_bulk')
async def use_pam_template_in_bulk(pam_forms: PamForms,
                                   response: Response,
                                   auth_result: str = Security(auth.verify)) -> BulkOutput:
    """
    Create a list of PAM-template documents - 
    a bulk operation. Max 50. This endpoint 
    will return a list of PDF/PNG/SVG bytestrings. 
    You need to parse the output 
    appropriately to get the list of the output files.
    """
    output_array, p_time_tot = _make_bulk(pam_forms, pam_template)
    response.headers["MIMI-Processing-Time"] = str(p_time_tot)
    return output_array
