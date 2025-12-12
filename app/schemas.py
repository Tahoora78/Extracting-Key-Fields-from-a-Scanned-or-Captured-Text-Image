from pydantic import BaseModel
from typing import Optional

class OCRTaskCreate(BaseModel):
    filename: str

class OCRTaskResult(BaseModel):
    id: int
    status: str
    title: Optional[str] = None
    date: Optional[str] = None
    code: Optional[str] = None
    error: Optional[str] = None
