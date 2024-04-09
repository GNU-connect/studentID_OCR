FROM python:3.11

# Python 패키지 설치
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tesseract 언어팩(kor) 다운로드 및 설치
RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata/ \
    && curl -L -o /usr/share/tesseract-ocr/4.00/tessdata/kor.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/kor.traineddata

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/kor.traineddata

WORKDIR /app

# 애플리케이션 코드 복사
COPY . .

EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--debug"]
