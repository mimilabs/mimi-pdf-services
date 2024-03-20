from pydantic import BaseModel

class RawTypst(BaseModel):
    source: str
    filename: str = "tmp"


