from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
import base64
import typst

class RawTypst(BaseModel):
    source: str
    name: str | None = None

app = FastAPI()

@app.post('/get_pdf_from_rawtypst')
async def get_pdf_from_rawtypst(rawtypst: RawTypst):
    
    name = 'tmp'
    if rawtypst.name: 
        name = rawtypst.name
    with open(f"tmp/{name}.typ", "w") as fp:
        fp.write(rawtypst.source)

    pdf_bytes = typst.compile(f"tmp/{name}.typ")
    #pdf_str = base64.b64encode(pdf_bytes).decode('utf-8')
    return Response(content=pdf_bytes, 
                    media_type="application/pdf", 
                    headers={"Content-Disposition": ('attachment; '+ 
                            f'filename={name}.pdf')})


