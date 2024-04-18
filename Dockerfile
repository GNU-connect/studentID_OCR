FROM python:3.11

WORKDIR /app

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tesseract 언어팩(kor) 다운로드 및 설치
RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata/ \
    && curl -L -o /usr/share/tesseract-ocr/4.00/tessdata/kor.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/kor.traineddata

# Python 패키지 설치
COPY requirements.txt .
RUN pip3 install --upgrade pip \
   &&  pip3 install --no-cache-dir -r requirements.txt --default-timeout=600

# 환경 변수 설정
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
ENV PYTHONUNBUFFERED 1
ENV SUPABASE_URL=${SUPABASE_URL}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV CARD_VARIFICATION_IMAGE_URL=${CARD_VARIFICATION_IMAGE_URL}

# 애플리케이션 코드 복사
COPY . .

EXPOSE 5000

CMD ["python", "-u", "app.py"]
