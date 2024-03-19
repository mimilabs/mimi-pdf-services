from fastapi import FastAPI, Response, Security
from fastapi.responses import FileResponse
from pydantic import BaseModel
import base64
import typst
from utils import VerifyToken
from pathlib import Path

app = FastAPI()
auth = VerifyToken()

class RawTypst(BaseModel):
    source: str
    filename: str = "tmp"


@app.post('/get_pdf_blank_template')
async def get_pdf_blank_template(rawtypst: RawTypst,
                    auth_result: str = Security(auth.verify)):
    
    filename = Path(rawtypst.filename).stem

    with open(f"typsources/onetime/{filename}.typ", "w") as fp:
        fp.write(rawtypst.source)
    pdf_bytes = typst.compile(f"typsources/onetime/{filename}.typ")
    return Response(content=pdf_bytes, 
                    media_type="application/pdf", 
                    headers={"Content-Disposition": ('attachment; '+ 
                            f'filename={filename}.pdf')})

