import os
from .celery_worker import celery
from .database import SessionLocal
from .models import OCRTask
from PIL import Image
import pytesseract
import re


@celery.task
def process_image(task_id: int):
    db = SessionLocal()
    task = db.query(OCRTask).filter(OCRTask.id == task_id).first()
    if not task:
        db.close()
        return

    file_path = task.filename 

    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        title = None
        code = None
        date = None

        code_pattern = re.compile(r"\b[A-Za-z]{1,4}\d{1,4}\b")
        date_pattern = re.compile(
            r"\b(\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})\b"
        )

        for line in lines:
            m = date_pattern.search(line)
            if m:
                date = m.group(1)
                break

        for line in lines:
            m = code_pattern.search(line)
            if m:
                code = m.group(0)
                break

        candidates = [
            line for line in lines
            if re.search(r"[A-Za-z]", line)
            and not date_pattern.search(line)
            and not code_pattern.search(line)
        ]

        if candidates:
            title = max(candidates, key=len)

        task.title = title
        task.code = code
        task.date = date

        if title and code and date:
            task.status = "success"
        else:
            task.status = "failed"
            task.error = f"Missing fields. OCR extracted:\n{text}"

    except Exception as e:
        task.status = "failed"
        task.error = str(e)

    finally:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as delete_error:
            print(f"Failed to delete file {file_path}: {delete_error}")

        db.commit()
        db.close()
