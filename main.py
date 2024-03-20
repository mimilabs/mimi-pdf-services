from fastapi import FastAPI, Response, Security
from fastapi.responses import FileResponse
from pydantic import BaseModel
import base64
import typst
from utils import VerifyToken
from pathlib import Path
import tempfile
import time
import os
from string import Template
from fastapi import HTTPException

app = FastAPI()
auth = VerifyToken()

basic_template = Template(open('templates/basic_template.typ').read())

class RawTypst(BaseModel):
    source: str
    filename: str = "tmp"

def _make_pdf(source: str, filename: str):
    
    start = time.time()    
    fpath = "./workdir" 
    
    # create a temp file to run Typst
    with tempfile.NamedTemporaryFile(dir="./workdir", 
                                     mode='w', delete=False) as fp:
        fp.write(source)
        fpath = fp.name

    try:
        pdf_bytes = typst.compile(fpath) # compile the Typst source
    except RuntimeError as e:
        raise HTTPException(status_code=500,
                            detail=str(e),
                            headers={"X-Error": "Typst compile error"})

    os.remove(fpath) # remove the temp file

    end = time.time() # measure the team
    processing_time = end - start
    
    # log on MongoDB
    return Response(content=pdf_bytes, 
                media_type="application/pdf", 
                headers={"Content-Disposition": ('attachment; '+ 
                                    f'filename={filename}.pdf'),
                     "MIMI-Processing-Time": str(processing_time),
                     "MIMI-MongoDB-ID": ""})


@app.post('/get_pdf_blank_template')
async def get_pdf_blank_template(rawtypst: RawTypst,
                    auth_result: str = Security(auth.verify)):
    filename = Path(rawtypst.filename).stem
    return _make_pdf(rawtypst.source, filename)

@app.post('/get_pdf_basic_template')
async def get_pdf_basic_template(rawtypst: RawTypst,
                    auth_result: str = Security(auth.verify)):
    start = time.time()    
    filename = Path(rawtypst.filename).stem
    return _make_pdf(basic_template.substitute(content=rawtypst.source),
                     filename)

