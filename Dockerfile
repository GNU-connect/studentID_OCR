FROM python:3.11

COPY pip.conf /root/.config/pip/pip.conf

ENV DEBIAN_FRONTEND=noninteractive

# Update and install depedencies
RUN apt-get update && \
    apt-get install -y wget unzip bc vim python3-pip libleptonica-dev git
RUN apt-get install -y --reinstall make && \
    apt-get install -y g++ autoconf automake libtool pkg-config libpng-dev libtiff5-dev libicu-dev \
        libpango1.0-dev autoconf-archive

WORKDIR /app
COPY requirements.txt .

# Tesseract 언어팩(kor) 다운로드 및 설치
RUN mkdir src && cd /app/src && \
    wget https://github.com/tesseract-ocr/tesseract/archive/5.3.3.zip && \
	unzip 5.3.3.zip && \
    cd /app/src/tesseract-5.1.0 && ./autogen.sh && ./configure && make && make install && ldconfig && \
    make training && make training-install && \
    cd /usr/local/share/tessdata && \
    wget https://github.com/tesseract-ocr/tessdata_best/raw/main/kor.traineddata

ENV TESSDATA_PREFIX=/usr/local/share/tessdata

# Python 패키지 설치
RUN pip3 install --upgrade pip \
   &&  pip3 install --no-cache-dir -r requirements.txt

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1

# 애플리케이션 코드 복사
COPY . .

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
