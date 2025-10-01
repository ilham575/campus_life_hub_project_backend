FROM python:3.11-slim

WORKDIR /app

# ติดตั้ง dependency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

# default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]