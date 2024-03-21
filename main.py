from fastapi import FastAPI, Response, Security
from fastapi.responses import FileResponse
import base64
import typst
from utils import VerifyToken
from pathlib import Path
import tempfile
import time
import os
from string import Template
from fastapi import HTTPException
from models import RawTypst, PrcForm

app = FastAPI()
auth = VerifyToken()

# load all templates
basic_template = Template(open('templates/basic_template.typ').read())
prc_template = Template(open('templates/prc_template.typ').read())

def _make_pdf(source: str, filename: str, format: str):
    
    start = time.time()    
    fpath = "./workdir" 
    
    # create a temp file to run Typst
    with tempfile.NamedTemporaryFile(dir="./workdir", 
                                     mode='w', delete=False) as fp:
        fp.write(source)
        fpath = fp.name

    try:
        pdf_bytes = typst.compile(fpath, format=format) # compile the Typst source
    except RuntimeError as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail=str(e),
                            headers={"X-Error": "Typst compile error"})

    os.remove(fpath) # remove the temp file

    end = time.time() # measure the team
    processing_time = end - start
    
    # log on MongoDB
    return Response(content=pdf_bytes, 
                media_type=f"application/{format}", 
                headers={"Content-Disposition": ('attachment; '+ 
                            f'filename={filename}.{format}'),
                     "MIMI-Processing-Time": str(processing_time),
                     "MIMI-MongoDB-ID": ""})


@app.post('/get_blank_template')
async def get_blank_template(rawtypst: RawTypst,
                    auth_result: str = Security(auth.verify)):
    filename = Path(rawtypst.filename).stem
    format = rawtypst.format
    return _make_pdf(rawtypst.source, filename, format)

@app.post('/get_basic_template')
async def get_basic_template(rawtypst: RawTypst,
                    auth_result: str = Security(auth.verify)):
    start = time.time()    
    filename = Path(rawtypst.filename).stem
    format = rawtypst.format
    return _make_pdf(basic_template.substitute(content=rawtypst.source),
                     filename, format)

@app.post('/get_prc_template')
async def get_basic_template(prcform: PrcForm,
                    auth_result: str = Security(auth.verify)):
    start = time.time()    
    filename = Path(prcform.filename).stem
    format = prcform.format
    return _make_pdf(prc_template.substitute(**prcform.__dict__),
                     filename, format)

