FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev poppler-utils bash && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

RUN mkdir /app/uploads

EXPOSE 8000

CMD ["bash", "-c", "export PYTHONPATH=/app && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
