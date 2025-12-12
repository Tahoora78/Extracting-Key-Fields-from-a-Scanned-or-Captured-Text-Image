from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from .database import Base, engine, get_db
from .models import OCRTask
from .schemas import OCRTaskResult
from .tasks import process_image
from fastapi.responses import JSONResponse
from fastapi import Depends

Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/upload-image/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = OCRTask(filename=filepath, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)

    process_image.delay(task.id)

    return {"id": task.id, "status": task.status}

@app.get("/api/ocr-tasks/{task_id}/result/", response_model=OCRTaskResult)
def get_result(task_id: int, db: Session = Depends(get_db)):
    task = db.query(OCRTask).filter(OCRTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return OCRTaskResult(
        id=task.id,
        status=task.status,
        title=task.title,
        date=task.date,
        code=task.code,
        error=task.error
    )
