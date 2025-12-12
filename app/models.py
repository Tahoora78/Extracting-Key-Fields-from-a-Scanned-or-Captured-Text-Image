from sqlalchemy import Column, Integer, String
from .database import Base

class OCRTask(Base):
    __tablename__ = "ocr_tasks"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    title = Column(String, nullable=True)
    date = Column(String, nullable=True)
    code = Column(String, nullable=True)
    status = Column(String, default="pending")
    error = Column(String, nullable=True)
