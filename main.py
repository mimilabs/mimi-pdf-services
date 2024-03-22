from fastapi import FastAPI, Response, Security
import base64
import typst
from utils import VerifyToken
from pathlib import Path
import tempfile
import time
import os
from string import Template
from fastapi import HTTPException
from models import BasicForm, BasicForms, PrcForm, PrcForms, BulkOutput
import base64

app = FastAPI(
        title = "mimi-pdf-services",
        summary = "mimi-pdf-services can generate a lot of PDFs very fast",
        description = """mimi-pdf-services is a light-weight and fast PDF generation
service. To use this service, you can ask info@mimilabs.ai to get the Auth0-based 
API key (easy) or you can download the source code and use the source code 
directly (hard, but more customaizable).""",
        version="0.0.1",
        contact={
            "name": "mimilabs.ai",
            "url": "https://mimilabs.ai",
            "email": "info@mimilabs.ai"
        },
        license_info ={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            }
        )
auth = VerifyToken() # use Auth0 API-Key

# work directory
# - this is the folder where raw Typst sources and image files are stored
WORK_DIR = "./workdir"

# load all templates
basic_template = Template(open('templates/basic_template.typ').read())
prc_template = Template(open('templates/prc_template.typ').read())

def _run_typst(source: str, format: str):
    
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

    os.remove(fpath) # remove the temp file

    end = time.time() # measure the compile + misc. time 
    processing_time = end - start

    return output, processing_time

def _make_single(source: str, filename: str, format: str):
    output, processing_time = _run_typst(source, format) 
    return Response(content=output, 
                media_type=f"application/{format}", 
                headers={"Content-Disposition": ('attachment; '+ 
                            f'filename={filename}.{format}'),
                     "MIMI-Processing-Time": str(processing_time)})

def _make_bulk(forms, template):
    output_array = [] 
    p_time_tot = 0
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


@app.post('/use_blank_template')
async def use_blank_template(basic_form: BasicForm,
                    auth_result: str = Security(auth.verify)) -> Response:
    """
    Create a document with no header and no footer; blank template.
    """
    return _make_single(basic_form.content, 
                        Path(basic_form.filename).stem,
                        basic_form.format)

@app.post('/use_basic_template')
async def use_basic_template(basic_form: BasicForm,
                    auth_result: str = Security(auth.verify)) -> Response:
    """
    Create a document with basic header and footer. The headerlogo and footertext
    parameters can be customizable. However, the headerlogo file should exist in 
    the work directory. 
    """
    return _make_single(basic_template.substitute(**basic_form.__dict__),
                        Path(basic_form.filename).stem,
                        basic_form.format)

@app.post('/use_prc_template')
async def use_prc_template(prc_form: PrcForm,
                    auth_result: str = Security(auth.verify)) -> Response:
    """
    Create a PRC-template document, where PRC stands for the Profile, Risk, and 
    Quality sections. However, one can change the PRC sections to any other names.
    For example, if you set `psection` as "Section A," the first section
    name will show as "Section A," not "Profile." The form is highly customizable.
    """
    return _make_single(prc_template.substitute(**prc_form.__dict__),
                        Path(prc_form.filename).stem,
                        prc_form.format)

@app.post('/use_blank_template_in_bulk')
async def use_blank_template_in_bulk(basic_forms: BasicForms,
                    response: Response,
                    auth_result: str = Security(auth.verify)) -> BulkOutput:
    """
    Create a list of blank-template documents - a bulk operation. This endpoint 
    will return a list of PDF/PNG/SVG bytestrings. You need to parse the output 
    appropriately to get the list of the output files.
    """
    output_array, p_time_tot = _make_bulk(basic_forms, blank_template)
    response.headers["MIMI-Processing-Time"] = str(p_time_tot)
    return output_array

@app.post('/use_basic_template_in_bulk')
async def use_basic_template_in_bulk(basic_forms: BasicForms,
                    response: Response,
                    auth_result: str = Security(auth.verify)) -> BulkOutput:
    """
    Create a list of basic-template documents - a bulk operation. This endpoint 
    will return a list of PDF/PNG/SVG bytestrings. You need to parse the output 
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
    Create a list of PRC-template documents - a bulk operation. This endpoint 
    will return a list of PDF/PNG/SVG bytestrings. You need to parse the output 
    appropriately to get the list of the output files.
    """
    output_array, p_time_tot = _make_bulk(prc_forms, prc_template)
    response.headers["MIMI-Processing-Time"] = str(p_time_tot)
    return output_array

