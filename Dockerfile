# Hafif ve kararlı bir Python imajı taban alınıyor
FROM python:3.10-slim

# Konteyner içindeki çalışma dizini ayarlanıyor
WORKDIR /app

# Bağımlılıklar kopyalanıyor ve yükleniyor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projenin tüm kodları konteyner içine kopyalanıyor
COPY . .

# FastAPI uygulamasını dış dünyaya açacak şekilde uvicorn başlatılıyor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]