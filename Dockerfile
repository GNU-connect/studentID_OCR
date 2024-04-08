FROM python:3.11

# tesseract-ocr, libtesseract-dev 설치
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-script-hang \
    tesseract-ocr-script-hang-vert \
    tesseract-ocr-script-kore \
    tesseract-ocr-script-kore-vert \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# Configure Poetry
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

# POETRY_REQUESTS_TIMEOUT 환경 변수를 설정하여 요청 타임아웃을 조정합니다.
ENV POETRY_REQUESTS_TIMEOUT=600

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev


COPY . /app
EXPOSE 5000
CMD [ "poetry", "run", "python", "-m", "flask", "run", "--host=0.0.0.0" ]