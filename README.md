# FastAPI OCR Processing System (with Celery, Redis & Docker)

This project is an OCR (Optical Character Recognition) processing system built using:

* **FastAPI** – REST API framework
* **Celery** – Background task queue
* **Redis** – Celery message broker
* **Tesseract OCR** – Image text extraction
* **SQLite** – Lightweight relational database
* **Docker & Docker Compose** – Containerized deployment

The application allows users to upload an image, automatically extract text (title, code, date), and retrieve structured results.

---

## ⚙️ Features

### ✔ Upload an image via REST API

Images are saved to the `/uploads` directory.

### ✔ Asynchronous OCR processing

Celery workers process OCR tasks in the background.

### ✔ Auto-extracts:

* **Title** — longest alphabetic text line
* **Code** — patterns like `cd01`, `AB123`, etc.
* **Date** — formats like `2025/12/12`, `2025-12-12`, and variants

### ✔ Results stored in SQLite

Accessible anytime via REST API.

### ✔ Fully containerized

Just run:

```bash
docker compose up --build
```

---

## 📤 API Usage

### 1. Upload an Image

**POST** `/api/upload-image/`

**Form-data:**

```
file: <image file>
```

**Example response:**

```json
{
  "id": 1,
  "status": "pending"
}
```

The OCR task is now running in Celery.

---

### 2. Fetch OCR Result

**GET** `/api/ocr-tasks/{task_id}/result/`

**Example successful result:**

```json
{
  "id": 1,
  "status": "success",
  "title": "Test Title",
  "code": "cd01",
  "date": "2025/12/12",
  "error": null
}
```

**Example failed extraction:**

```json
{
  "id": 3,
  "status": "failed",
  "title": null,
  "code": null,
  "date": null,
  "error": "Unable to extract required fields."
}
```

---

## 🧠 OCR Logic Summary

The Celery worker uses Tesseract to extract text, then applies logic to determine fields:

* **Date:** detected using multiple regex formats
* **Code:** alphanumeric pattern with letters + digits
* **Title:** longest alphabetic text line, independent of layout

This ensures robust detection even when the position of the date, code, or title varies.

---

## 📦 Project Structure

```
project/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── workers/
│   ├── utils/
│   └── main.py
├── celery_worker/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Running the Project

### Development

```
docker compose up --build
```

### Stopping containers

```
docker compose down
```

---


## 📄 License

MIT License — free to use and modify.
